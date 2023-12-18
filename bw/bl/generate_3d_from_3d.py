import numpy as np
import logging
import bpy
import bmesh
import bw.bl.get_quantile_colors as bwqc
import bw.bl.add_text as add_text
import bw.bl.create_rectangle as cr
import bw.bl.clear_all_objects as bwclear
import bw.bl.assign_color as assign_color
import bw.bl.assign_material as assign_material
import bw.bl.decimator_on_object as decimator
import bw.sk.profile_data_with_cubes as bwmc


log = logging.getLogger(__name__)


def generate_3d_from_3d(
    data: np.ndarray,
    target_faces: int = None,
    mask: np.ndarray = None,
    name: str = None,
    name_color: str = "#FFFFFF",
    name_opacity: float = 1.0,
    name_extrude: float = 1.7,
    desc: str = None,
    desc_color: str = "#555555",
    desc_opacity: float = 1.0,
    desc_extrude: float = 1.5,
    x: float = 0.0,
    y: float = 0.0,
    z: float = 0.0,
    vertex_scale_size: float = 1.0,
    color_percentile: float = 95.0,
    background_enabled: bool = False,
    background_color: str = "#000000",
    background_opacity: float = 1.0,
    background_height: int = None,
    background_width: int = None,
    background_depth: int = None,
    background_x: float = None,
    background_y: float = None,
    background_z: float = None,
    level: float = 1.0,
    step_size: int = 1,
    clean_workspace: bool = False,
    target_mb: float = None,
    mc_report_file: str = None,
    mesh_idx: int = None,
    num_colors: int = 5,
    decimation_ratio: float = None,
    safe_for_colors_in_ram: bool = False,
):
    """
    generate_3d_from_3d

    generate a marching cubes representation
    of the underlying 3d data based off statistical
    relevance in the float32 data.

    supports targeting colors in the mesh based
    off a target percentile in the z-axis value of
    the source 3d array

    returns tuple (
        mesh_name,
        closest_report,
    )

    :param data: 3d array data
    :param target_faces: optional - find the nearest
        marching cubes configuration by resulting
        number of faces in the volume
    :param mask: 3d array for mask
    :param name: optional - name for labeling the
        mesh to the left
    :param name_color: hex color string for the name text
    :param name_opacity: opacity for the name text
    :param name_extrude: extusion amount for the name text
    :param desc: optional - description for labeling the
        mesh to the left
    :param desc_color: hex color string for the desc text
    :param desc_opacity: opacity for the desc text
    :param desc_extrude: extusion amount for the name text
    :param x: x position for the mesh
    :param y: y position for the mesh
    :param z: z position for the mesh
    :param level: level for the marching
        cubes algorithm
    :param vertex_scale_size: apply a scaler to each vertex
    :param color_percentile: target percentile
        for applying a color to a cube face
    :param background_enabled: flag for including
        drawing a rectangle under the mesh
        (and optional text)
    :param background_color: hex color string
        with default #000000 for black
    :param background_opacity: transparency for
        the background
        with default no transparency at 1.0
    :param background_height: how tall is the background
    :param background_width: how wide is the background
    :param background_depth: how deep is the background
    :param background_x: x position for the background
    :param background_y: y position for the background
    :param background_z: z position for the background
    :param step_size: number of marching cube step sizes
    :param clean_workspace: flag for deleting all
        objects before rendering
    :param target_mb: optional - find the nearest
        marching cubes configuration by resulting
        megabyte size (more useful to use
        target_faces)
    :param mc_report_file: optional - path to save
        the mc_report slim dictionary as a json
        file
    :param num_colors: optional - number of
        different colors (too many colors will
        cause the mesh to fail drawing)
    :param decimation_ratio: reduce each
        layer this percentage with supported values between
        0.0 and 1.0
    :param safe_for_colors_in_ram: flag to
        force-enable colors. coloring this much
        data is very expensive so it is off
        by default
    """

    # for debugging
    if clean_workspace:
        bwclear.clear_all_objects()
    if not mesh_idx:
        mesh_idx = 1

    mesh_name = f"Mesh_{mesh_idx}"
    mesh_obj_name = f"MeshObj_{mesh_idx}"

    # Create a new mesh
    mesh = bpy.data.meshes.new(name=mesh_name)
    mesh_obj = bpy.data.objects.new(mesh_obj_name, mesh)

    # Link the mesh to the scene
    bpy.context.scene.collection.objects.link(mesh_obj)
    bpy.context.view_layer.objects.active = mesh_obj

    mesh_obj.select_set(True)

    # Flip the array to have the desired orientation (x, z, y)
    data = np.transpose(data, (0, 2, 1))

    # Apply marching cubes algorithm and build a report
    mc_report = bwmc.profile_data_with_cubes(
        data=data,
        data_name=name,
        target_mb=target_mb,
        target_faces=target_faces,
        save_to_file=mc_report_file,
        include_vertices=True,
        include_normals=True,
        include_faces=True,
        include_masks=True,
    )
    if mc_report is None:
        mc_report = bwmc.profile_data_with_cubes(
            data=data,
            data_name=name,
            target_mb=target_mb,
            target_faces=1000,
            save_to_file=mc_report_file,
            include_vertices=True,
            include_normals=True,
            include_faces=True,
            include_masks=True,
        )
        if mc_report is None:
            log.debug(
                "failed to find a marching cube profile for "
                f"name={name}"
            )
            return (
                mesh_name,
                None,
            )

    # Find the closest report based off the target
    closest_report = mc_report["closest"]
    if len(closest_report) == 0:
        log.error(
            "failed to find a marching cube configuration "
            f"name={name} "
            f"that targets faces={target_faces} "
            f"size_mb={target_mb} "
            "stopping"
        )
        # raise SystemExit
        return (
            mesh_name,
            None,
        )
    vertices = closest_report["vertices"]
    faces = closest_report["faces"]
    # normals = closest_report['normals']
    mc_z_values = closest_report["z_values"]
    closest_level = closest_report["level"]
    closest_step_size = closest_report["step_size"]
    closest_desc = closest_report["desc"]
    num_vertices = len(vertices)
    num_faces = len(faces)
    log.debug(
        f"mc {closest_desc} target_faces={target_faces} "
        f"level={closest_level} "
        f"step_size{closest_step_size} "
        f"from src data.shape={data.shape} "
        f"cubes z_values.shape={mc_z_values.shape} "
        f"vertices={num_vertices} "
        f"faces={num_faces} "
        f"level={level} step_size={step_size} "
        f"decimation={decimation_ratio} "
        "calculated "
        ""
    )
    z_values = mc_z_values

    mesh.from_pydata(vertices, [], faces)
    mesh.update()

    # reduce the mesh marching cube complexity
    if decimation_ratio:
        if 0.0 < decimation_ratio < 1.0:
            if False:
                decimator.apply_decimator(
                    name=mesh_obj_name,
                    decimation_ratio=decimation_ratio,
                )
        else:
            log.error(
                f"invalid decimation_ratio={decimation_ratio} "
                "only values between 0.0 and 1.0 "
                "are supported"
            )

    # Create a BMesh
    bm = bmesh.new()

    # Create vertices
    log.debug(
        "rendering mesh "
        f"vertices={len(vertices)} "
        f"faces={len(faces)}"
    )

    # scale the vertices
    for v in vertices:
        bm.verts.new(
            (
                v[0] * vertex_scale_size,
                v[1] * vertex_scale_size,
                v[2] * vertex_scale_size,
            )
        )

    # Ensure lookup table for vertices
    bm.verts.ensure_lookup_table()

    # Create faces
    for f in faces[:-3]:
        bm.faces.new([bm.verts[i] for i in f])

    # Ensure lookup table for faces
    bm.faces.ensure_lookup_table()

    # determine colors based off the min/max values
    # in the z-axis

    # use the face's z weights to
    min_values = []
    max_values = []
    z_values = []
    z_min = None
    z_max = None
    num_faces = len(faces)
    if num_faces > 5000:
        if safe_for_colors_in_ram:
            log.critical(
                "warning consider disabling colors to save on ram "
                f"for num_faces={num_faces}"
            )
    if safe_for_colors_in_ram:
        log.debug(f"colorizing num_faces={num_faces}")
        for face in bm.faces:
            z_values_face = np.array(
                [v.co.z for v in face.verts]
            )
            z_min = np.min(z_values_face)
            z_max = np.max(z_values_face)
            break

        for face in bm.faces:
            z_values_face = np.array(
                [v.co.z for v in face.verts]
            )
            if z_values_face.size > 0:
                cur_min = np.min(z_values_face)
                cur_max = np.max(z_values_face)
                if z_min > cur_min:
                    z_min = cur_min
                    # add the min to the front
                    min_values.insert(0, cur_min)
                else:
                    min_values.append(cur_min)
                if z_max < cur_max:
                    z_max = cur_max
                    # add the max to the end
                    max_values.append(cur_max)
                else:
                    max_values.insert(0, cur_max)
        # partially-sorted z_values
        z_values = np.array(min_values + max_values)

        if z_min:
            z_min -= 1.0
        if z_max:
            z_max += 1.0
        log.debug(
            f"using face z_values: {z_values} "
            f"[{z_min},{z_max}]"
        )
        # get build the colors based off the max/min
        color_dict = bwqc.get_quantile_colors(
            min_value=z_min,
            max_value=z_max,
            num=num_colors,
            opacity=0.5,
            z_values=z_values,
        )

        # total_weight = np.sum(z_values)

        # Colorize faces based on weighted percentile
        for face in bm.faces:
            z_values_face = np.array(
                [v.co.z for v in face.verts]
            )
            # Change to desired percentile
            weighted_percentile = np.percentile(
                z_values_face, color_percentile
            )
            color = assign_color.assign_color(
                weighted_percentile, color_dict
            )
            # if you hit this, you cannot draw anymore faces/colors
            # try/ex will just run out of ram
            face.material_index = (
                assign_material.assign_material(color, mesh)
            )
    # if able to support coloring with ram

    # Set the location of the object
    mesh_x = x
    mesh_y = y
    mesh_z = z
    if name:
        add_text.add_text(
            text=name,
            position=(x, y, z),
            color=name_color,
            opacity=name_opacity,
            extrude=name_extrude,
        )
        mesh_z += 5
        mesh_x += 20
    if desc:
        desc_x = x
        desc_y = y
        desc_z = z
        if name:
            desc_x = x
            desc_y = y - 10
            desc_z = z
        add_text.add_text(
            text=desc,
            position=(desc_x, desc_y, desc_z),
            color=desc_color,
            opacity=desc_opacity,
            extrude=desc_extrude,
        )

    mesh_obj.location = (mesh_x, mesh_y, mesh_z)

    # Update the BMesh and free it
    bm.to_mesh(mesh)
    bm.free()

    # Create the background if enabled
    if background_enabled:
        if not background_x:
            background_x = x - 2
        if not background_y:
            background_y = y - 2
        if not background_z:
            background_z = z
        if not background_height:
            background_height = mesh_y + 200
        if not background_width:
            background_width = 200
        if not background_depth:
            background_depth = 2
        log.debug(
            f"drawing background({background_x}, "
            f"{background_y}, {background_z}) "
            f"dim=({background_height}, "
            f"{background_width}, "
            f"{background_depth})"
        )
        cr.create_rectangle(
            height=background_height,
            width=background_width,
            depth=background_depth,
            hex_color=background_color,
            opacity=background_opacity,
            x_position=background_x,
            y_position=background_y,
            z_position=background_z,
        )
    return (
        mesh_name,
        closest_report,
    )
