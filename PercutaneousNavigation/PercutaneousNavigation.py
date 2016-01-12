import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging
import math

#
# PercutaneousNavigation
#

class PercutaneousNavigation(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "PercutaneousNavigation" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Examples"]
    self.parent.dependencies = []
    self.parent.contributors = ["D. Garcia-Mato (Laboratorio de Imagen Medica, Madrid, Spain)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
    This is an example of scripted loadable module bundled in an extension.
    It performs a simple thresholding on the input volume and optionally captures a screenshot.
    """
    self.parent.acknowledgementText = """
    This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
    and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
    """ # replace with organization, grant and thanks.

#
# PercutaneousNavigationWidget
#

class PercutaneousNavigationWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    self.PercutaneousNavigationLogic = PercutaneousNavigationLogic() 

    self.defaultStyleSheet = "QLabel { color : #000000; \
                                       font: bold 14px}"

    # Transform Definition Area
    transformsCollapsibleButton = ctk.ctkCollapsibleButton()
    transformsCollapsibleButton.text = "Transforms"
    self.layout.addWidget(transformsCollapsibleButton)   
    parametersFormLayout = qt.QFormLayout(transformsCollapsibleButton)
    
    # ReferenceToTracker transform selector
    self.referenceToTrackerSelector = slicer.qMRMLNodeComboBox()
    self.referenceToTrackerSelector.nodeTypes = ( ("vtkMRMLLinearTransformNode"), "" )
    self.referenceToTrackerSelector.selectNodeUponCreation = True
    self.referenceToTrackerSelector.addEnabled = False
    self.referenceToTrackerSelector.removeEnabled = False
    self.referenceToTrackerSelector.noneEnabled = False
    self.referenceToTrackerSelector.showHidden = False
    self.referenceToTrackerSelector.showChildNodeTypes = False
    self.referenceToTrackerSelector.setMRMLScene( slicer.mrmlScene )
    self.referenceToTrackerSelector.setToolTip( "Pick the ReferenceToTracker transform." )
    parametersFormLayout.addRow("ReferenceToTracker transform: ", self.referenceToTrackerSelector)
    
    # TrackerToReference transform selector
    self.trackerToReferenceSelector = slicer.qMRMLNodeComboBox()
    self.trackerToReferenceSelector.nodeTypes = ( ("vtkMRMLLinearTransformNode"), "" )
    self.trackerToReferenceSelector.selectNodeUponCreation = True
    self.trackerToReferenceSelector.addEnabled = False
    self.trackerToReferenceSelector.removeEnabled = False
    self.trackerToReferenceSelector.noneEnabled = False
    self.trackerToReferenceSelector.showHidden = False
    self.trackerToReferenceSelector.showChildNodeTypes = False
    self.trackerToReferenceSelector.setMRMLScene( slicer.mrmlScene )
    self.trackerToReferenceSelector.setToolTip( "Pick the TrackerToReference transform." )
    parametersFormLayout.addRow("TrackerToReference transform: ", self.trackerToReferenceSelector)

    # PointerToTracker transform selector
    self.pointerToTrackerSelector = slicer.qMRMLNodeComboBox()
    self.pointerToTrackerSelector.nodeTypes = ( ("vtkMRMLLinearTransformNode"), "" )
    self.pointerToTrackerSelector.selectNodeUponCreation = True
    self.pointerToTrackerSelector.addEnabled = False
    self.pointerToTrackerSelector.removeEnabled = False
    self.pointerToTrackerSelector.noneEnabled = False
    self.pointerToTrackerSelector.showHidden = False
    self.pointerToTrackerSelector.showChildNodeTypes = False
    self.pointerToTrackerSelector.setMRMLScene( slicer.mrmlScene )
    self.pointerToTrackerSelector.setToolTip( "Pick the PointerToTracker transform." )
    parametersFormLayout.addRow("PointerToTracker transform: ", self.pointerToTrackerSelector)

    # PointerTipToPointer transform selector
    self.pointerTipToPointerSelector = slicer.qMRMLNodeComboBox()
    self.pointerTipToPointerSelector.nodeTypes = ( ("vtkMRMLLinearTransformNode"), "" )
    self.pointerTipToPointerSelector.selectNodeUponCreation = True
    self.pointerTipToPointerSelector.addEnabled = False
    self.pointerTipToPointerSelector.removeEnabled = False
    self.pointerTipToPointerSelector.noneEnabled = False
    self.pointerTipToPointerSelector.showHidden = False
    self.pointerTipToPointerSelector.showChildNodeTypes = False
    self.pointerTipToPointerSelector.setMRMLScene( slicer.mrmlScene )
    self.pointerTipToPointerSelector.setToolTip( "Pick the PointerTipToPointer transform." )
    parametersFormLayout.addRow("PointerTipToPointer transform: ", self.pointerTipToPointerSelector)

    # NeedleToTracker transform selector
    self.needleToTrackerSelector = slicer.qMRMLNodeComboBox()
    self.needleToTrackerSelector.nodeTypes = ( ("vtkMRMLLinearTransformNode"), "" )
    self.needleToTrackerSelector.selectNodeUponCreation = True
    self.needleToTrackerSelector.addEnabled = False
    self.needleToTrackerSelector.removeEnabled = False
    self.needleToTrackerSelector.noneEnabled = False
    self.needleToTrackerSelector.showHidden = False
    self.needleToTrackerSelector.showChildNodeTypes = False
    self.needleToTrackerSelector.setMRMLScene( slicer.mrmlScene )
    self.needleToTrackerSelector.setToolTip( "Pick the NeedleToTracker transform." )
    parametersFormLayout.addRow("NeedleToTracker transform: ", self.needleToTrackerSelector)

    # NeedleTipToNeedle transform selector
    self.needleTipToNeedleSelector = slicer.qMRMLNodeComboBox()
    self.needleTipToNeedleSelector.nodeTypes = ( ("vtkMRMLLinearTransformNode"), "" )
    self.needleTipToNeedleSelector.selectNodeUponCreation = True
    self.needleTipToNeedleSelector.addEnabled = False
    self.needleTipToNeedleSelector.removeEnabled = False
    self.needleTipToNeedleSelector.noneEnabled = False
    self.needleTipToNeedleSelector.showHidden = False
    self.needleTipToNeedleSelector.showChildNodeTypes = False
    self.needleTipToNeedleSelector.setMRMLScene( slicer.mrmlScene )
    self.needleTipToNeedleSelector.setToolTip( "Pick the NeedleTipToNeedle transform." )
    parametersFormLayout.addRow("NeedleTipToNeedle transform: ", self.needleTipToNeedleSelector)

    # Apply Transforms For Registration Button
    self.applyTransformsForRegistrationButton = qt.QPushButton("Apply Transforms For Registration")
    self.applyTransformsForRegistrationButton.toolTip = "Apply selected transforms."
    self.applyTransformsForRegistrationButton.enabled = False
    parametersFormLayout.addRow(self.applyTransformsForRegistrationButton)

    # PatientToReference transform selector
    self.patientToReferenceSelector = slicer.qMRMLNodeComboBox()
    self.patientToReferenceSelector.nodeTypes = ( ("vtkMRMLLinearTransformNode"), "" )
    self.patientToReferenceSelector.selectNodeUponCreation = True
    self.patientToReferenceSelector.addEnabled = False
    self.patientToReferenceSelector.removeEnabled = False
    self.patientToReferenceSelector.noneEnabled = False
    self.patientToReferenceSelector.showHidden = False
    self.patientToReferenceSelector.showChildNodeTypes = False
    self.patientToReferenceSelector.setMRMLScene( slicer.mrmlScene )
    self.patientToReferenceSelector.setToolTip( "Pick the PatientToReference transform." )
    parametersFormLayout.addRow("PatientToReference transform: ", self.patientToReferenceSelector)

    # Apply Transforms For Navigation Button
    self.applyTransformsForNavigationButton = qt.QPushButton("Apply Transforms For Navigation")
    self.applyTransformsForNavigationButton.toolTip = "Apply selected transforms."
    self.applyTransformsForNavigationButton.enabled = False
    parametersFormLayout.addRow(self.applyTransformsForNavigationButton)

    # Navigation Area
    navigationCollapsibleButton = ctk.ctkCollapsibleButton()
    navigationCollapsibleButton.text = "Navigation"
    self.layout.addWidget(navigationCollapsibleButton)   
    parametersFormLayout = qt.QFormLayout(navigationCollapsibleButton)

    # Soft Tissue Visibility Button
    self.softTissueVisibilityButton = qt.QPushButton()
    self.softTissueVisibilityButton.toolTip = "Soft tissue visibility."
    self.softTissueVisibilityButton.enabled = True
    self.softTissueVisibilityButtonState = 0
    self.softTissueVisibilityButtonStateText0 = "Make Soft Tissue Invisible"
    self.softTissueVisibilityButtonStateText1 = "Make Soft Tissue Visible"
    self.softTissueVisibilityButton.setText(self.softTissueVisibilityButtonStateText0)
    parametersFormLayout.addRow(self.softTissueVisibilityButton)

    # Bone Visibility Button
    self.boneVisibilityButton = qt.QPushButton()
    self.boneVisibilityButton.toolTip = "Bone visibility."
    self.boneVisibilityButton.enabled = True
    self.boneVisibilityButtonState = 0
    self.boneVisibilityButtonStateText0 = "Make Bone Invisible"
    self.boneVisibilityButtonStateText1 = "Make Bone Visible"
    self.boneVisibilityButton.setText(self.boneVisibilityButtonStateText0)
    parametersFormLayout.addRow(self.boneVisibilityButton)
    
    # Calculate Distance Button
    self.calculateDistanceButton = qt.QPushButton("Calculate Distance")
    self.calculateDistanceButton.enabled = True
    self.calculateDistanceButton.checkable = True
    parametersFormLayout.addRow(self.calculateDistanceButton)   

    # Calculate Distance Label
    self.calculateDistanceLabel = qt.QLabel('-')
    self.calculateDistanceLabel.setStyleSheet(self.defaultStyleSheet)
    self.QFormLayoutLabel = qt.QLabel('Distance to target (mm): ')
    self.QFormLayoutLabel.setStyleSheet(self.defaultStyleSheet)
    parametersFormLayout.addRow(self.QFormLayoutLabel, self.calculateDistanceLabel) 

    # Needle Viewpoint Button
    self.needleViewpointButton = qt.QPushButton()
    self.needleViewpointButton.toolTip = "Apply needle viewpoint."
    self.needleViewpointButton.enabled = True
    self.enableNeedleViewpointButtonState = 0
    self.enableNeedleViewpointButtonTextState0 = "Enable Viewpoint Mode"
    self.enableNeedleViewpointButtonTextState1 = "Disable Viewpoint Mode"
    self.needleViewpointButton.setText(self.enableNeedleViewpointButtonTextState0)
    parametersFormLayout.addRow(self.needleViewpointButton)

    # connections
    self.referenceToTrackerSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelectForRegistration)
    self.trackerToReferenceSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelectForRegistration)
    self.pointerToTrackerSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelectForRegistration)
    self.pointerTipToPointerSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelectForRegistration)
    self.needleToTrackerSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelectForRegistration)
    self.needleTipToNeedleSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelectForRegistration)
    self.applyTransformsForRegistrationButton.connect('clicked(bool)', self.onApplyTransformsForRegistrationClicked)
    self.patientToReferenceSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelectForNavigation)
    self.applyTransformsForNavigationButton.connect('clicked(bool)', self.onApplyTransformsForNavigationClicked)
    self.softTissueVisibilityButton.connect('clicked(bool)', self.onSoftTissueVisibilityButtonClicked)
    self.boneVisibilityButton.connect('clicked(bool)', self.onBoneVisibilityButtonClicked)
    self.calculateDistanceButton.connect('clicked(bool)', self.onCalculateDistanceClicked)
    self.needleViewpointButton.connect('clicked(bool)', self.onNeedleViewpointButtonClicked)
    
    # Add vertical spacer
    self.layout.addStretch(1)

    # Load models
    PercutaneousNavigationModuleDataPath = slicer.modules.PercutaneousNavigation.path.replace("PercutaneousNavigation.py","") + 'Resources/Models/'
    self.boneModel = slicer.util.getNode('BoneModel')
    if not self.boneModel:
        slicer.util.loadModel(PercutaneousNavigationModuleDataPath + 'BoneModel.stl')
        self.boneModel = slicer.util.getNode(pattern="BoneModel")
        self.boneModelDisplay=self.boneModel.GetModelDisplayNode()
        self.boneModelDisplay.SetColor([1,1,1])

    self.softTissueModel = slicer.util.getNode('SoftTissueModel')
    if not self.softTissueModel:
        slicer.util.loadModel(PercutaneousNavigationModuleDataPath + 'SoftTissueModel.stl')
        self.softTissueModel = slicer.util.getNode(pattern="SoftTissueModel")
        self.softTissueModelDisplay=self.softTissueModel.GetModelDisplayNode()
        self.softTissueModelDisplay.SetColor([1,0.7,0.53])

    self.needleModel = slicer.util.getNode('NeedleModel')
    if not self.needleModel:
        slicer.util.loadModel(PercutaneousNavigationModuleDataPath + 'NeedleModel.stl')
        self.needleModel = slicer.util.getNode(pattern="NeedleModel")
        self.needleModelDisplay=self.needleModel.GetModelDisplayNode()
        self.needleModelDisplay.SetColor([0,1,1])

    self.pointerModel = slicer.util.getNode('PointerModel')
    if not self.pointerModel:
        slicer.util.loadModel(PercutaneousNavigationModuleDataPath + 'PointerModel.stl')
        self.pointerModel = slicer.util.getNode(pattern="PointerModel")
        self.pointerModelDisplay=self.pointerModel.GetModelDisplayNode()
        self.pointerModelDisplay.SetColor([0,0,0])
    
  def cleanup(self):
    pass

  def onSelectForRegistration(self):
    self.applyTransformsForRegistrationButton.enabled = self.referenceToTrackerSelector.currentNode() and self.trackerToReferenceSelector.currentNode() and self.pointerToTrackerSelector.currentNode() and self.pointerTipToPointerSelector.currentNode() and self.needleToTrackerSelector.currentNode() and self.needleTipToNeedleSelector.currentNode() 
  
  def onSelectForNavigation(self):
    self.applyTransformsForNavigationButton.enabled = True

  def onApplyTransformsForRegistrationClicked(self):
    self.referenceToTrackerSelector.enabled = False
    self.trackerToReferenceSelector.enabled = False
    self.pointerToTrackerSelector.enabled = False
    self.pointerTipToPointerSelector.enabled = False
    self.needleToTrackerSelector.enabled = False
    self.needleTipToNeedleSelector.enabled = False
    self.applyTransformsForRegistrationButton.enabled = False
    self.PercutaneousNavigationLogic.buildTransformTreeForRegistration(self.boneModel, self.softTissueModel, self.pointerModel, self.needleModel, self.trackerToReferenceSelector.currentNode(), self.pointerToTrackerSelector.currentNode(), self.pointerTipToPointerSelector.currentNode(), self.needleToTrackerSelector.currentNode(), self.needleTipToNeedleSelector.currentNode())
  
  def onApplyTransformsForNavigationClicked(self):
    self.patientToReferenceSelector.enabled = False
    self.applyTransformsForNavigationButton.enabled = False
    self.PercutaneousNavigationLogic.resetTransformTree(self.boneModel, self.softTissueModel, self.pointerModel, self.needleModel, self.pointerToTrackerSelector.currentNode())
    self.PercutaneousNavigationLogic.buildTransformTreeForNavigation(self.boneModel, self.softTissueModel, self.pointerModel, self.needleModel, self.referenceToTrackerSelector.currentNode(), self.pointerToTrackerSelector.currentNode(), self.pointerTipToPointerSelector.currentNode(), self.needleToTrackerSelector.currentNode(), self.needleTipToNeedleSelector.currentNode(),self.patientToReferenceSelector.currentNode())
  
  def onSoftTissueVisibilityButtonClicked(self):
    if self.softTissueVisibilityButtonState == 0:
          self.softTissueModelDisplay.VisibilityOff()
          self.softTissueVisibilityButtonState = 1
          self.softTissueVisibilityButton.setText(self.softTissueVisibilityButtonStateText1)
    else: 
          self.softTissueModelDisplay.VisibilityOn()
          self.softTissueVisibilityButtonState = 0
          self.softTissueVisibilityButton.setText(self.softTissueVisibilityButtonStateText0)

  def onBoneVisibilityButtonClicked(self):
    if self.boneVisibilityButtonState == 0:
          self.boneModelDisplay.VisibilityOff()
          self.boneVisibilityButtonState = 1
          self.boneVisibilityButton.setText(self.boneVisibilityButtonStateText1)
    else: 
          self.boneModelDisplay.VisibilityOn()
          self.boneVisibilityButtonState = 0
          self.boneVisibilityButton.setText(self.boneVisibilityButtonStateText0)
          
  def onCalculateDistanceClicked(self):
    self.PercutaneousNavigationLogic.setOutPutDistanceLabel(self.calculateDistanceLabel)
    if self.calculateDistanceButton.checked:
      self.PercutaneousNavigationLogic.transformTargetFiducial(self.patientToReferenceSelector.currentNode(), self.referenceToTrackerSelector.currentNode())
      self.PercutaneousNavigationLogic.SetMembers(self.needleTipToNeedleSelector.currentNode(), self.needleToTrackerSelector.currentNode())
      self.PercutaneousNavigationLogic.addCalculateDistanceObserver()  
    elif not self.calculateDistanceButton.checked:
      self.PercutaneousNavigationLogic.callbackObserverTag=0        
      self.PercutaneousNavigationLogic.removeCalculateDistanceObserver()
      # slicer.mrmlScene.RemoveNode(self.PercutaneousNavigationLogic.line) 

  def onNeedleViewpointButtonClicked(self):
    if self.enableNeedleViewpointButtonState == 0:
          self.PercutaneousNavigationLogic.SetNeedleViewpoint(self.needleModel, self.needleToTrackerSelector.currentNode())
          self.PercutaneousNavigationLogic.StartViewpoint()
          self.enableNeedleViewpointButtonState = 1
          self.needleViewpointButton.setText(self.enableNeedleViewpointButtonTextState1)
    else: 
          self.PercutaneousNavigationLogic.StopViewpoint()
          self.enableNeedleViewpointButtonState = 0
          self.needleViewpointButton.setText(self.enableNeedleViewpointButtonTextState0)

      
#
# PercutaneousNavigationLogic
#

class PercutaneousNavigationLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """
  def __init__(self):
    self.toolTipToTool = slicer.util.getNode('toolTipToTool')
    if not self.toolTipToTool:
      self.toolTipToTool=slicer.vtkMRMLLinearTransformNode()
      self.toolTipToTool.SetName("toolTipToTool")
      m = vtk.vtkMatrix4x4()
      m.SetElement( 0, 0, 1 ) # Row 1
      m.SetElement( 0, 1, 0 )
      m.SetElement( 0, 2, 0 )
      m.SetElement( 0, 3, 0 )      
      m.SetElement( 1, 0, 0 )  # Row 2
      m.SetElement( 1, 1, 1 )
      m.SetElement( 1, 2, 0 )
      m.SetElement( 1, 3, 0 )       
      m.SetElement( 2, 0, 0 )  # Row 3
      m.SetElement( 2, 1, 0 )
      m.SetElement( 2, 2, 1 )
      m.SetElement( 2, 3, 0 )
      self.toolTipToTool.SetMatrixTransformToParent(m)
      slicer.mrmlScene.AddNode(self.toolTipToTool)

    self.toolToReference = slicer.util.getNode('toolToReference')
    if not self.toolToReference:
      self.toolToReference=slicer.vtkMRMLLinearTransformNode()
      self.toolToReference.SetName("toolToReference")
      matrixRef = vtk.vtkMatrix4x4()
      matrixRef.SetElement( 0, 0, 1 ) # Row 1
      matrixRef.SetElement( 0, 1, 0 )
      matrixRef.SetElement( 0, 2, 0 )
      matrixRef.SetElement( 0, 3, 0 )      
      matrixRef.SetElement( 1, 0, 0 )  # Row 2
      matrixRef.SetElement( 1, 1, 1 )
      matrixRef.SetElement( 1, 2, 0 )
      matrixRef.SetElement( 1, 3, 0 )       
      matrixRef.SetElement( 2, 0, 0 )  # Row 3
      matrixRef.SetElement( 2, 1, 0 )
      matrixRef.SetElement( 2, 2, 1 )
      matrixRef.SetElement( 2, 3, 0 )
      self.toolToReference.SetMatrixTransformToParent(matrixRef)
      slicer.mrmlScene.AddNode(self.toolToReference)
   
    self.tipFiducial = slicer.util.getNode('Tip')
    if not self.tipFiducial:
      self.tipFiducial = slicer.vtkMRMLMarkupsFiducialNode()  
      self.tipFiducial.SetName('Tip')
      self.tipFiducial.AddFiducial(0, 0, 0)
      self.tipFiducial.SetNthFiducialLabel(0, '')
      slicer.mrmlScene.AddNode(self.tipFiducial)
      self.tipFiducial.SetDisplayVisibility(True)
      self.tipFiducial.GetDisplayNode().SetGlyphType(1) # Vertex2D
      self.tipFiducial.GetDisplayNode().SetTextScale(1.3)
      self.tipFiducial.GetDisplayNode().SetSelectedColor(1,1,1)

    self.targetFiducial = slicer.util.getNode('Target')
    if not self.targetFiducial:
      self.targetFiducial = slicer.vtkMRMLMarkupsFiducialNode()  
      self.targetFiducial.SetName('Target')
      self.targetFiducial.AddFiducial(0, 0, 0)
      self.targetFiducial.SetNthFiducialLabel(0, '')
      slicer.mrmlScene.AddNode(self.targetFiducial)
      self.targetFiducial.SetDisplayVisibility(True)
      self.targetFiducial.GetDisplayNode().SetGlyphType(1) # Vertex2D
      self.targetFiducial.GetDisplayNode().SetTextScale(1.3)
      self.targetFiducial.GetDisplayNode().SetSelectedColor(1,1,1)
      
    self.line = slicer.util.getNode('Line')
    if not self.line:
      self.line = slicer.vtkMRMLModelNode()
      self.line.SetName('Line')
      linePolyData = vtk.vtkPolyData()
      self.line.SetAndObservePolyData(linePolyData)      
      modelDisplay = slicer.vtkMRMLModelDisplayNode()
      modelDisplay.SetSliceIntersectionVisibility(True)
      modelDisplay.SetColor(0,1,0)
      slicer.mrmlScene.AddNode(modelDisplay)      
      self.line.SetAndObserveDisplayNodeID(modelDisplay.GetID())      
      slicer.mrmlScene.AddNode(self.line)
      
    # VTK objects
    self.transformPolyDataFilter = vtk.vtkTransformPolyDataFilter()
    self.cellLocator = vtk.vtkCellLocator()
    
    # 3D View
    threeDWidget = slicer.app.layoutManager().threeDWidget(0)
    self.threeDView = threeDWidget.threeDView()
    
    self.callbackObserverTag = -1
    self.observerTag=None

    # Output Distance Label
    self.outputDistanceLabel=None

    import Viewpoint # Viewpoint Module must have been added to Slicer 
    self.viewpointLogic = Viewpoint.ViewpointLogic()

    # Camera transformations
    self.needleCameraToNeedle = slicer.util.getNode('needleCameraToNeedle')
    if not self.needleCameraToNeedle:
      self.needleCameraToNeedle=slicer.vtkMRMLLinearTransformNode()
      self.needleCameraToNeedle.SetName("needleCameraToNeedle")
      m = vtk.vtkMatrix4x4()
       
      m.SetElement( 0, 0, -0.05 ) # Row 1
      m.SetElement( 0, 1, 0.09 )
      m.SetElement( 0, 2, -0.99 )
      m.SetElement( 0, 3, 60.72 )      
      m.SetElement( 1, 0, -0.01 )  # Row 2
      m.SetElement( 1, 1, 1 )
      m.SetElement( 1, 2, 0.09 )
      m.SetElement( 1, 3, 12.17 )       
      m.SetElement( 2, 0, 1 )  # Row 3
      m.SetElement( 2, 1, 0.01 )
      m.SetElement( 2, 2, -0.05 )
      m.SetElement( 2, 3, -7.26 )

      self.needleCameraToNeedle.SetMatrixTransformToParent(m)
      slicer.mrmlScene.AddNode(self.needleCameraToNeedle)


  def SetNeedleViewpoint(self, NeedleModelNode, NeedleToTrackerTransformNode):
    if NeedleToTrackerTransformNode:
      self.needleCameraToNeedle.SetAndObserveTransformNodeID(NeedleToTrackerTransformNode.GetID())  
      NeedleModelNode.GetDisplayNode().SetOpacity(1)

      SceneCameraNode=slicer.util.getNode('Default Scene Camera')
      
      # Viewpoint
      self.viewpointLogic.setCameraNode(SceneCameraNode)
      self.viewpointLogic.setTransformNode(self.needleCameraToNeedle)
      # self.viewpointLogic.setModelPOVOnNode(pointerModelNode)
      # self.viewpointLogic.setModelPOVOffNode(self.modelOnlyViewpointOffSelector.currentNode())
      # self.viewpointLogic.setTargetModelNode(pointerModelNode)
      # self.viewpointLogic.SetCameraXPosMm(53)
      # self.viewpointLogic.SetCameraYPosMm(72)
      # self.viewpointLogic.SetCameraZPosMm(119)
      self.viewpointLogic.startViewpoint()
      # self.initViewpoint(pointerModelNode, PointerToTrackerTransformNode)

      # NeedleModelNode.GetDisplayNode().SetVisibility (True);

  def StartViewpoint(self):
    self.viewpointLogic.startViewpoint()

  def StopViewpoint(self):
    # self.camera.SetAndObserveTransformNodeID(None)    
    self.viewpointLogic.stopViewpoint()
     
  def buildTransformTreeForRegistration(self, boneModelNode, softTissueModelNode, pointerModelNode, needleModelNode, trackerToReferenceTransformNode, pointerToTrackerTransformNode, pointerTipToPointerTransformNode, needleToTrackerTransformNode, needleTipToNeedleTransformNode):
    # Pointer
    pointerModelNode.SetAndObserveTransformNodeID(pointerTipToPointerTransformNode.GetID())
    pointerTipToPointerTransformNode.SetAndObserveTransformNodeID(pointerToTrackerTransformNode.GetID())
    pointerToTrackerTransformNode.SetAndObserveTransformNodeID(trackerToReferenceTransformNode.GetID())

    # Needle
    needleModelNode.SetAndObserveTransformNodeID(needleTipToNeedleTransformNode.GetID())
    needleTipToNeedleTransformNode.SetAndObserveTransformNodeID(needleToTrackerTransformNode.GetID())

  def buildTransformTreeForNavigation (self, boneModelNode, softTissueModelNode, pointerModelNode, needleModelNode, referenceToTrackerTransformNode, pointerToTrackerTransformNode, pointerTipToPointerTransformNode, needleToTrackerTransformNode, needleTipToNeedleTransformNode, patientToReferenceTransformNode):
    # Pointer
    pointerModelNode.SetAndObserveTransformNodeID(pointerTipToPointerTransformNode.GetID())
    pointerTipToPointerTransformNode.SetAndObserveTransformNodeID(pointerToTrackerTransformNode.GetID())
    
    # Needle
    needleModelNode.SetAndObserveTransformNodeID(needleTipToNeedleTransformNode.GetID())
    needleTipToNeedleTransformNode.SetAndObserveTransformNodeID(needleToTrackerTransformNode.GetID())

    # Patient
    boneModelNode.SetAndObserveTransformNodeID(patientToReferenceTransformNode.GetID())
    softTissueModelNode.SetAndObserveTransformNodeID(patientToReferenceTransformNode.GetID())
    patientToReferenceTransformNode.SetAndObserveTransformNodeID(referenceToTrackerTransformNode.GetID())

  def resetTransformTree(self, boneModelNode, softTissueModelNode, pointerModelNode, needleModelNode, pointerToTrackerTransformNode):
     # Reset transform tree
    pointerModelNode.SetAndObserveTransformNodeID(None)
    needleModelNode.SetAndObserveTransformNodeID(None)
    pointerModelNode.SetAndObserveTransformNodeID(None)
    needleModelNode.SetAndObserveTransformNodeID(None)
    pointerToTrackerTransformNode.SetAndObserveTransformNodeID(None)
  
  def SetMembers(self, toolTipToTool, toolToReference):
    self.toolTipToTool = toolTipToTool
    self.toolToReference = toolToReference
    
  def addCalculateDistanceObserver(self):
    print("[TEST] addCalculateDistanceObserver")
    if self.callbackObserverTag == -1:
      self.tipFiducial.SetAndObserveTransformNodeID(self.toolTipToTool.GetID())
      self.observerTag = self.toolToReference.AddObserver('ModifiedEvent', self.calculateCallback) # slicer.vtkMRMLMarkupsNode.MarkupAddedEvent
      logging.info('addCalculateDistanceObserver')
      
  def removeCalculateDistanceObserver(self):
    print("[TEST] removeCalculateDistanceObserver")
    self.callbackObserverTag = 1
    if self.callbackObserverTag != -1:
      self.toolToReference.RemoveObserver(self.observerTag)
      self.callbackObserverTag = -1
      logging.info('removeCalculateDistanceObserver')
      
  def calculateCallback(self, transformNode, event=None):
    self.calculateDistance()

  def calculateDistance(self):
    tipPoint = [0.0,0.0,0.0]
    targetPoint = [0.0, 0.0, 0.0]

    m = vtk.vtkMatrix4x4()
    self.toolTipToTool.GetMatrixTransformToWorld(m)
    tipPoint[0] = m.GetElement(0, 3)
    tipPoint[1] = m.GetElement(1, 3)
    tipPoint[2] = m.GetElement(2, 3)

    self.targetFiducial.GetNthFiducialPosition (1, targetPoint)
    # print(targetPoint)

    # Prueba David
    needlePoint = [0.0, 0.0, 0.0]
    v = vtk.vtkMatrix4x4()
    self.toolToReference.GetMatrixTransformToWorld(v)
    needlePoint[0] = v.GetElement(0, 3)
    needlePoint[1] = v.GetElement(1, 3)
    needlePoint[2] = v.GetElement(2, 3)
    # print(needlePoint)

    distance = math.sqrt(math.pow(tipPoint[0]-targetPoint[0], 2) + math.pow(tipPoint[1]-targetPoint[1], 2) + math.pow(tipPoint[2]-targetPoint[2], 2))
    
    self.outputDistanceLabel.setText('%.1f' % distance)

    self.drawLineBetweenPoints(tipPoint, targetPoint)
    
  def drawLineBetweenPoints(self, point1, point2):        
    # Create a vtkPoints object and store the points in it
    points = vtk.vtkPoints()
    points.InsertNextPoint(point1)
    points.InsertNextPoint(point2)

    # Create line
    line = vtk.vtkLine()
    line.GetPointIds().SetId(0,0) 
    line.GetPointIds().SetId(1,1)
    lineCellArray = vtk.vtkCellArray()
    lineCellArray.InsertNextCell(line)
    
    # Update model data
    self.line.GetPolyData().SetPoints(points)
    self.line.GetPolyData().SetLines(lineCellArray)

  def setOutPutDistanceLabel(self, label):
    self.outputDistanceLabel = label

  def transformTargetFiducial(self, patientToReferenceTransformNode, referenceToTrackerTransformNode):
    self.targetFiducial.SetAndObserveTransformNodeID(patientToReferenceTransformNode.GetID())
      






class PercutaneousNavigationTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_PercutaneousNavigation1()