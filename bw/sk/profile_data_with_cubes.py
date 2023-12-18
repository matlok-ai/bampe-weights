import os
import logging
import json
import numpy as np
from skimage.measure import marching_cubes
import bw.pp as pp


log = logging.getLogger(__name__)


def profile_data_with_cubes(
    data: np.ndarray,
    target_mb: float = None,
    target_faces: int = None,
    levels: list = None,
    steps: list = None,
    masks: list = None,
    include_vertices: bool = True,
    include_normals: bool = True,
    include_faces: bool = True,
    include_masks: bool = True,
    data_name: str = None,
    save_to_file: str = None,
):
    """
    uses marching cubes to profile the 3d data
    array. returns a list of dictionaries
    reporting profiles about the data with a
    **closest** key holding the nearest profile
    based off the **target_faces** argument.

    - supports finding the values that are
        closest to the target_mb without going
        over
    - optional flags for returning various slices
        of the marching cubes returned values and
        vertices, normals, faces, z_values and the
        mask that was used (if set)
    - supports saving the report diction as a
        json file to the save_to_file path

    :param data: numpy 3d ndarray of data
        to profile
    :param target_mb: optional - determine the
        marching cube configuration that is the
        closest to the megabyte size without going
        over
    :param target_faces: optional - determine the
        marching cube configuration that is the
        closest to the number of faces without going
        over
    :param levels: optional - levels to profile
    :param steps: optional - steps to profile
    :param masks: optional - masks to filter the data
    :param include_vertices: optional - flag to include
        vertices in the report node
    :param include_normals: optional - flag to include normals
        in the report nodes
    :param include_faces: optional - flag to include faces
        in the report nodes
    :param include_masks: optional - flag to include masks
        in the report nodes
    :param data_name: optional - label for tracking
        issues ingesting data
    :param save_to_file: optional - path to save the
        report for reviewing later
    :return: a report dictionary from the analysis

        ```
        report = {
            "size_mb": mb_size,
            "size": f"{mb_size}mb",
            "levels": levels,
            "step_sizes": steps,
            "masks": masks,
            "num_rows": num_rows,
            "num_cols": num_cols,
            "num_levels": num_levels,
            "num_steps": num_steps,
            "num_masks": num_masks,
            "num_reports": 0,
            "closest": {},
            "reports": []
        }
        ```
    """
    if not levels:
        levels = [0] + [i / 10.0 for i in range(0, 21)]
    if not steps:
        steps = [1, 2, 3, 4, 5, 6, 7, 10, 20]
    if not masks:
        masks = [None]

    num_levels = len(levels)
    num_steps = len(steps)
    num_masks = len(masks)
    num_rows = data.shape[0]
    num_cols = data.shape[1]

    src_mb_size = (
        float(4.0 * num_rows * num_cols) / 1024.0 / 1024.0
    )
    mb_size = float(f"{src_mb_size:.2f}")
    report = {
        "size_mb": mb_size,
        "size": f"{mb_size}mb",
        "levels": levels,
        "step_sizes": steps,
        "masks": masks,
        "num_rows": num_rows,
        "num_cols": num_cols,
        "num_levels": num_levels,
        "num_steps": num_steps,
        "num_masks": num_masks,
        "num_reports": 0,
        "closest": {},
        "reports": [],
    }
    if include_masks:
        report["masks"] = masks
    closest_report = None
    closest_dist_size = None
    closest_dist_faces = None
    closest_size = None
    closest_faces = None
    vertices = None
    faces = None
    mc_z_values = None
    total_reports = len(levels) * len(steps) * len(masks)
    report_idx = 1
    for level_idx, level in enumerate(levels):
        for step_size_idx, step_size in enumerate(steps):
            for mask_idx, mask in enumerate(masks):
                log.debug(
                    f"mc {report_idx}/{total_reports} "
                    f"name={data_name} "
                    "start "
                    f"target_mb={target_mb}mb "
                    f"data={data.shape} "
                    f"level={level} "
                    f"step_size={step_size} "
                    f"mask={mask} "
                    ""
                )
                report_idx += 1
                try:
                    (
                        vertices,
                        faces,
                        normals,
                        mc_z_values,
                    ) = marching_cubes(
                        data,
                        level=level,
                        step_size=step_size,
                        mask=mask,
                    )
                    report_node = {
                        "size_mb": None,
                        "size": None,
                        "level": level,
                        "step_size": step_size,
                        "mask": mask,
                        "num_vertices": 0,
                        "vertices": [],
                        "num_faces": 0,
                        "faces": [],
                        "num_normals": 0,
                        "normals": [],
                        "z_values": mc_z_values,
                        "num_z_values": len(mc_z_values),
                    }
                    num_vertices = len(vertices)
                    num_normals = len(normals)
                    num_faces = len(faces)
                    if not num_faces:
                        log.debug(
                            f"mc {report_idx}/{total_reports} "
                            f"name={data_name} "
                            "no shapes"
                            f"level_idx={level_idx} "
                            f"level={level} "
                            f"step_idx={step_size_idx} "
                            f"step_size={step_size} "
                            "no shapes"
                        )
                        continue
                    if include_vertices:
                        report_node["vertices"] = vertices
                        report_node[
                            "num_vertices"
                        ] = num_vertices
                    if include_faces:
                        report_node["faces"] = faces
                        report_node["num_faces"] = num_faces
                    if include_normals:
                        report_node["normals"] = normals
                        report_node[
                            "num_normals"
                        ] = num_normals
                    mc_mb_size_org = (
                        (float(4.0 * num_faces))
                        / 1024.0
                        / 1024.0
                    )
                    mc_mb_size = float(
                        f"{mc_mb_size_org:.2f}"
                    )
                    report_node["size_mb"] = mc_mb_size
                    report_node["size"] = f"{mc_mb_size}mb"
                    desc = (
                        f"analyzed {mb_size}mb "
                        f"calc {mc_mb_size}mb"
                    )
                    report_node["desc"] = desc
                    log.debug(
                        f"mc {report_idx}/{total_reports} "
                        f"name={data_name} "
                        f"level_idx={level_idx} "
                        f"{desc} "
                        f"level={level} "
                        f"step_idx={step_size_idx} "
                        f"step_size={step_size} "
                        f"verts={num_vertices} "
                        f"faces={num_faces} "
                        f"normals={num_normals} "
                        f"target_mb={target_mb} "
                        f"target_faces={target_faces} "
                        f"closest_dist_size={closest_dist_size} "
                        f"closest_dist_faces={closest_dist_faces} "
                        ""
                    )
                    if target_mb:
                        current_dist_size = float(
                            f"{float(target_mb - mc_mb_size):.2f}"
                        )
                        if current_dist_size < 0.0:
                            current_dist_size *= -1.0
                        if not closest_size:
                            closest_report = report_node
                            closest_size = mc_mb_size
                            closest_dist_size = (
                                current_dist_size
                            )
                        else:
                            """
                            log.info(
                                '     TEST SIZE '
                                f'cur {mc_mb_size} >= {target_mb} '
                                'AND '
                                f'dist {current_dist_size} < {closest_dist_size}')
                            """
                            if (
                                mc_mb_size >= target_mb
                            ) and (
                                current_dist_size
                                < closest_dist_size
                            ):
                                closest_report = report_node
                                closest_size = mc_mb_size
                                closest_dist_size = (
                                    current_dist_size
                                )
                                closest_faces = num_faces
                                log.debug(
                                    f"mc {report_idx}/{total_reports} "
                                    f"name={data_name} "
                                    f"level_idx={level_idx} "
                                    f"{desc} "
                                    f"level={level} "
                                    f"step_idx={step_size_idx} "
                                    f"step_size={step_size} "
                                    f"verts={num_vertices} "
                                    f"faces={num_faces} "
                                    f"normals={num_normals} "
                                    f"closest={closest_size}mb "
                                    f"closest_dist_size={closest_dist_size}mb "
                                    ""
                                )
                    if target_faces:
                        current_dist_faces = int(
                            target_faces - num_faces
                        )
                        log.debug(
                            "     TEST FACES "
                            f"{closest_faces} >= {target_faces} "
                            "AND "
                            f"dist {current_dist_faces} < {closest_dist_faces}"
                        )
                        if current_dist_faces < 0:
                            current_dist_faces *= -1
                        if not closest_faces:
                            closest_report = report_node
                            closest_faces = num_faces
                            closest_dist_faces = (
                                current_dist_faces
                            )
                        else:
                            log.debug(
                                "     TEST FACES "
                                f"{closest_faces} >= {target_faces} "
                                "AND "
                                f"dist {current_dist_faces} < {closest_dist_faces}"
                            )
                            if (
                                num_faces >= target_faces
                            ) and (
                                current_dist_faces
                                < closest_dist_faces
                            ):
                                closest_dist_faces = (
                                    current_dist_faces
                                )
                                closest_report = report_node
                                closest_size = mc_mb_size
                                closest_faces = num_faces

                    report["reports"].append(report_node)
                except Exception as e:
                    err_msg = str(e)
                    if err_msg not in [
                        "No surface found at the given iso value.",
                        "Surface level must be within volume data range.",
                    ]:
                        log.error(
                            f"mc {report_idx}/{total_reports} "
                            f"name={data_name} "
                            f"level_idx={level_idx} "
                            f"level={level} "
                            f"step_idx={step_size_idx} "
                            f"step_size={step_size} "
                            f'ex="{e}"'
                        )
                        raise e
                # end try/ex
            # for all masks
        # for all step_sizes
    # for all levels
    num_reports = len(report["reports"])
    report["num_reports"] = num_reports
    slim_report = {
        "size_mb": mb_size,
        "size": f"{mb_size}mb",
        "levels": levels,
        "step_sizes": steps,
        "num_rows": num_rows,
        "num_cols": num_cols,
        "num_reports": num_reports,
        "num_levels": num_levels,
        "num_steps": num_steps,
        "num_masks": num_masks,
        "target_mb": target_mb,
        "closest": {},
        "reports": [],
    }
    if not closest_report:
        if not target_faces:
            closest_report = report["reports"][0]
            all_undersized = True
            most_faces_report = None
            for report_node in report["reports"]:
                if not most_faces_report:
                    most_faces_report = report_node
                if report_node["num_faces"] > 10000:
                    all_undersized = False
                mfr = most_faces_report["num_faces"]
                rntf = report_node["num_faces"]
                if mfr < rntf:
                    most_faces_report = report_node
            if most_faces_report:
                log.debug(
                    "no closest report detected - "
                    "using most faces report"
                )
                mc_mb_size = most_faces_report["size_mb"]
                mb_size = most_faces_report["size"]
                desc = (
                    f"analyzed {mb_size}mb "
                    f"calc {mc_mb_size}mb"
                )
                closest_report = {
                    "desc": desc,
                    "size_mb": mc_mb_size,
                    "size": f"{mc_mb_size}mb",
                    "level": most_faces_report["level"],
                    "step_size": most_faces_report[
                        "step_size"
                    ],
                    "mask": most_faces_report["mask"],
                    "num_vertices": most_faces_report[
                        "num_vertices"
                    ],
                    "vertices": most_faces_report[
                        "vertices"
                    ],
                    "num_faces": most_faces_report[
                        "num_faces"
                    ],
                    "faces": most_faces_report["faces"],
                    "num_normals": most_faces_report[
                        "num_normals"
                    ],
                    "normals": most_faces_report["normals"],
                    "z_values": most_faces_report[
                        "z_values"
                    ],
                    "num_z_values": most_faces_report[
                        "num_z_values"
                    ],
                }
            elif all_undersized:
                log.debug(
                    "no closest report detected - "
                    "using default marching cubes"
                )
                (
                    vertices,
                    faces,
                    normals,
                    mc_z_values,
                ) = marching_cubes(
                    data,
                )
                mc_mb_size_org = (
                    (float(4.0 * len(faces)))
                    / 1024.0
                    / 1024.0
                )
                mc_mb_size = float(f"{mc_mb_size_org:.2f}")
                desc = (
                    f"analyzed {mb_size}mb "
                    f"calc {mc_mb_size}mb"
                )
                closest_report = {
                    "desc": desc,
                    "size_mb": mc_mb_size,
                    "size": f"{mc_mb_size}mb",
                    "level": None,
                    "step_size": None,
                    "mask": None,
                    "num_vertices": len(vertices),
                    "vertices": vertices,
                    "num_faces": len(faces),
                    "faces": faces,
                    "num_normals": len(normals),
                    "normals": normals,
                    "z_values": mc_z_values,
                    "num_z_values": len(mc_z_values),
                }
        else:
            log.debug(
                "trying to find nearest "
                f"faces={target_faces}"
            )
            # try to find the nearest from below
            # the target_faces
            found_report = False
            for ridx, report_node in enumerate(
                report["reports"]
            ):
                detected_faces = report_node["num_faces"]
                log.debug(
                    f"layer={data_name} mc {ridx} "
                    f"faces={detected_faces}"
                )
                if (detected_faces > 0) and (
                    detected_faces < target_faces
                ):
                    closest_report = report_node
                    found_report = True
            if not found_report:
                cur_data_min = np.min(data)
                cur_data_max = np.max(data)
                if cur_data_max == cur_data_min:
                    log.debug(
                        "ignored data due to match - "
                        f"name={data_name} "
                        f"data_min={(np.min(data))} "
                        f"data_max={(np.max(data))} "
                    )
                else:
                    if target_faces == 1000:
                        log.debug(
                            "unsupported data that failed "
                            "marching cubes "
                            f"target_faces={target_faces} "
                            f"name={data_name} "
                            f"data_min={(np.min(data))} "
                            f"data_max={(np.max(data))} "
                        )
                return None

        # end of trying to find one by the nearest
    # if no closest found so far

    # end of trying to find the closest
    if closest_report:
        slim_report["closest"] = {
            "level": closest_report["level"],
            "step_size": closest_report["step_size"],
            "num_vertices": closest_report["num_vertices"],
            "num_faces": closest_report["num_faces"],
            "num_normals": closest_report["num_normals"],
            "num_z_values": closest_report["num_z_values"],
            "desc": closest_report["desc"],
            "size_mb": closest_report["size_mb"],
            "size": closest_report["size"],
        }
        report["closest"] = closest_report
    else:
        log.error(
            f"failed to find closest with report={num_reports} "
            f"from levels={num_levels} "
            f"steps={num_steps} "
            f"reports={pp.pp(slim_report)} "
            ""
        )
    keys_to_copy = [
        "size_mb",
        "size",
        "desc",
        "level",
        "step_size",
        "num_vertices",
        "num_faces",
        "num_normals",
        "num_z_values",
    ]
    if save_to_file:
        log.debug(
            f"saving {total_reports} to {save_to_file}"
        )
        for report_node in report["reports"]:
            new_node = {}
            for key in keys_to_copy:
                new_node[key] = report_node[key]
            slim_report["reports"].append(new_node)
        with open(save_to_file, "w") as fp:
            fp.write(json.dumps(slim_report))
        if not os.path.exists(save_to_file):
            log.error(
                f"failed saving {total_reports} reports "
                f"to {save_to_file}"
            )
    if False:
        log.info(
            f"calculated {num_reports} from levels={num_levels} "
            f"steps={num_steps} "
            f"reports={pp.pp(slim_report)} "
            ""
        )
    return report
