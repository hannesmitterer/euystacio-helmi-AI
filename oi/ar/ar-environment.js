/**
 * OI: Open Interface - AR Environment Manager
 * Manages augmented reality workspace allocation and rendering
 */

import * as THREE from 'three';

class AREnvironment {
  constructor(containerElement) {
    this.container = containerElement;
    this.scene = null;
    this.camera = null;
    this.renderer = null;
    this.workspaces = new Map();
    this.activeWorkspace = null;
    this.isInitialized = false;
  }

  /**
   * Initialize Three.js AR environment
   */
  initialize() {
    if (this.isInitialized) return;

    // Create scene
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x0a0a0a);

    // Create camera
    this.camera = new THREE.PerspectiveCamera(
      75,
      this.container.clientWidth / this.container.clientHeight,
      0.1,
      1000
    );
    this.camera.position.z = 5;

    // Create renderer
    this.renderer = new THREE.WebGLRenderer({ antialias: true });
    this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    this.container.appendChild(this.renderer.domElement);

    // Add ambient light
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    this.scene.add(ambientLight);

    // Add directional light
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(5, 5, 5);
    this.scene.add(directionalLight);

    // Handle window resize
    window.addEventListener('resize', () => this.handleResize());

    this.isInitialized = true;
    this.animate();
  }

  /**
   * Handle window resize
   * @private
   */
  handleResize() {
    if (!this.camera || !this.renderer) return;

    this.camera.aspect = this.container.clientWidth / this.container.clientHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
  }

  /**
   * Animation loop
   * @private
   */
  animate() {
    requestAnimationFrame(() => this.animate());

    // Rotate active workspace if exists
    if (this.activeWorkspace) {
      const workspace = this.workspaces.get(this.activeWorkspace);
      if (workspace && workspace.mesh) {
        workspace.mesh.rotation.y += 0.005;
      }
    }

    this.renderer.render(this.scene, this.camera);
  }

  /**
   * Allocate a new AR workspace
   * @param {string} workspaceId - Unique workspace identifier
   * @param {Object} config - Workspace configuration
   * @returns {Object} Workspace object
   */
  allocateWorkspace(workspaceId, config = {}) {
    if (this.workspaces.has(workspaceId)) {
      return this.workspaces.get(workspaceId);
    }

    const workspace = {
      id: workspaceId,
      owner: config.owner || 'anonymous',
      createdAt: Date.now(),
      mesh: this.createWorkspaceMesh(config),
      objects: [],
      collaborators: []
    };

    this.workspaces.set(workspaceId, workspace);
    this.scene.add(workspace.mesh);

    return workspace;
  }

  /**
   * Create a visual mesh for the workspace
   * @private
   */
  createWorkspaceMesh(config) {
    const geometry = new THREE.BoxGeometry(2, 2, 2);
    const material = new THREE.MeshPhongMaterial({
      color: config.color || 0x0f766e,
      transparent: true,
      opacity: 0.6
    });

    const mesh = new THREE.Mesh(geometry, material);
    
    // Add wireframe
    const wireframe = new THREE.LineSegments(
      new THREE.EdgesGeometry(geometry),
      new THREE.LineBasicMaterial({ color: 0xffffff })
    );
    mesh.add(wireframe);

    return mesh;
  }

  /**
   * Set active workspace
   * @param {string} workspaceId - Workspace ID to activate
   * @returns {boolean} Success status
   */
  setActiveWorkspace(workspaceId) {
    if (!this.workspaces.has(workspaceId)) {
      return false;
    }

    this.activeWorkspace = workspaceId;
    
    // Focus camera on active workspace
    const workspace = this.workspaces.get(workspaceId);
    if (workspace.mesh) {
      this.camera.lookAt(workspace.mesh.position);
    }

    return true;
  }

  /**
   * Add 3D object to workspace
   * @param {string} workspaceId - Target workspace
   * @param {THREE.Object3D} object - 3D object to add
   * @param {Object} metadata - Object metadata
   */
  addObjectToWorkspace(workspaceId, object, metadata = {}) {
    const workspace = this.workspaces.get(workspaceId);
    if (!workspace) return false;

    const objectData = {
      id: metadata.id || `obj_${Date.now()}`,
      mesh: object,
      metadata,
      addedAt: Date.now()
    };

    workspace.objects.push(objectData);
    workspace.mesh.add(object);

    return objectData;
  }

  /**
   * Create a file representation in AR space
   * @param {Object} fileInfo - File information
   * @returns {THREE.Object3D} 3D file representation
   */
  createFileObject(fileInfo) {
    const group = new THREE.Group();

    // Create file icon
    const geometry = new THREE.PlaneGeometry(0.5, 0.7);
    const material = new THREE.MeshPhongMaterial({
      color: 0x3b82f6,
      side: THREE.DoubleSide
    });
    const plane = new THREE.Mesh(geometry, material);
    group.add(plane);

    // Add file name label (simplified - in real implementation use text texture)
    const labelGeometry = new THREE.PlaneGeometry(0.5, 0.1);
    const labelMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
    const label = new THREE.Mesh(labelGeometry, labelMaterial);
    label.position.y = -0.4;
    group.add(label);

    group.userData = fileInfo;

    return group;
  }

  /**
   * Add collaborator to workspace
   * @param {string} workspaceId - Workspace ID
   * @param {string} userId - User ID
   * @param {Object} userData - User data
   */
  addCollaborator(workspaceId, userId, userData = {}) {
    const workspace = this.workspaces.get(workspaceId);
    if (!workspace) return false;

    const collaborator = {
      id: userId,
      ...userData,
      joinedAt: Date.now()
    };

    workspace.collaborators.push(collaborator);
    return collaborator;
  }

  /**
   * Remove workspace
   * @param {string} workspaceId - Workspace to remove
   */
  removeWorkspace(workspaceId) {
    const workspace = this.workspaces.get(workspaceId);
    if (!workspace) return false;

    this.scene.remove(workspace.mesh);
    this.workspaces.delete(workspaceId);

    if (this.activeWorkspace === workspaceId) {
      this.activeWorkspace = null;
    }

    return true;
  }

  /**
   * Get workspace information
   * @param {string} workspaceId - Workspace ID
   * @returns {Object|null} Workspace info
   */
  getWorkspaceInfo(workspaceId) {
    const workspace = this.workspaces.get(workspaceId);
    if (!workspace) return null;

    return {
      id: workspace.id,
      owner: workspace.owner,
      createdAt: workspace.createdAt,
      objectCount: workspace.objects.length,
      collaborators: workspace.collaborators.map(c => ({
        id: c.id,
        joinedAt: c.joinedAt
      }))
    };
  }

  /**
   * Cleanup and dispose resources
   */
  dispose() {
    // Remove all workspaces
    this.workspaces.forEach((workspace, id) => {
      this.removeWorkspace(id);
    });

    // Dispose renderer
    if (this.renderer) {
      this.renderer.dispose();
      if (this.container.contains(this.renderer.domElement)) {
        this.container.removeChild(this.renderer.domElement);
      }
    }

    this.isInitialized = false;
  }
}

export default AREnvironment;
