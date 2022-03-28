from ast import arg
from typing import Optional, Union
from DICOMLib import DICOMUtils
import slicer
import vtk
import sys
import numpy as np

def load_dicom_data() -> list:
    """
    return: nodes list
    """
    dicomData = r'C:\Users\andro\Documents\dicoms\native'
    nodes = []

    with DICOMUtils.TemporaryDICOMDatabase() as db:
        DICOMUtils.importDicom(dicomData, db)
        patientUIDs = db.patients()
        for patient in patientUIDs:
            nodes.extend(DICOMUtils.loadPatientByUID(patient))

    
    return nodes


def load_tumor_node(nodes_list: list, number_of_node: int) -> None:
    volumeNode = slicer.util.getNode(nodes_list[number_of_node])
    tumorNode = slicer.util.loadVolume(r'C:\Users\andro\Documents\PycharmProjects\Bachelor\resources\Segmentation.nrrd')


def get_tumor_voxels(node) -> np.ndarray:
    return slicer.util.arrayFromVolume(node)


def get_bone_voxels(arr: np.ndarray) -> np.ndarray:
    return (((arr >= 300) & (arr <= 1900)) * 1)


def generate_sphere_on_pos(x: float, y: float, z:float, r: float) -> vtk.vtkSphereSource():
    sphere = vtk.vtkSphereSource()
    sphere.SetCenter(x, y, z)
    sphere.SetRadius(r)
    slicer.modules.models.logic().AddModel(sphere.GetOutputPort())
    return sphere


#TODO: do something with this dude
volRenLogic = slicer.modules.volumerendering.logic()
displayNode = volRenLogic.CreateDefaultVolumeRenderingNodes(tumorNode)
volRenLogic.SetDefaultRenderingMethod("VTKGPURayCast")
displayNode.SetVisibility(True)

model.GetDisplayNode().SetOpacity(0.4)
model.GetDisplayNode().SetColor(1,0,1)


def get_ijk_to_ras_matrix(node) -> vtk.vtkMatrix4x4():
    ijk_ras = vtk.vtkMatrix4x4()
    node.GetIJKToRASMatrix(ijk_ras)
    return ijk_ras


def get_convex_hull(tumor_voxels: np.ndarray) -> vtk.vtkPoints():
    p = np.where(tumor_voxels != 0)
    points = vtk.vtkPoints()
    for i in range(len(p[0])):
        points.InsertNextPoint(p[0][i], p[1][i], p[2][i])


    #TODO: finish func


def calculate_center_of_mass(tumor_voxels: np.ndarray, tumor_node) -> tuple:
    """
    return: tuple with center of mass' xyz coords
    """

    #TODO: create func
    cm = vtk.vtkCenterOfMass()

    polyData = vtk.vtkPolyData()
    polyData.SetPoints(points)
    cm.SetInputData(polyData)
    cm.SetUseScalarsAsWeights(False)
    cm.Update()
    centerOfTumor = list(cm.GetCenter())
    ijk_ras = get_ijk_to_ras_matrix(tumor_node)
    ras_center = tuple(ijk_ras.MultiplyFloatPoint([*centerOfTumor, 1])[:-1])
    return ras_center


def main():
    pass


if __name__ == "__main__":
    main()
