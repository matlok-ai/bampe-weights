import bpy


def assign_material(
    color,
    mesh,
):
    """
    assign_material

    assign a color tuple to a material in blender

    returns int for the new number of materials in the mesh
    """
    # Create a new material with the specified color
    mat = bpy.data.materials.new(
        name=f"Material_{len(bpy.data.materials)}"
    )
    mat.use_nodes = (
        False  # Disable node-based materials for simplicity
    )
    mat.diffuse_color = color
    mesh.materials.append(mat)

    # Return the material index
    return len(mesh.materials) - 1
