using UnityEngine;

public class PhysicsHands : MonoBehaviour {
    [SerializeField] GameObject followObject;
    [SerializeField] float followSpeed = 30f;
    [SerializeField] float rotateSpeed = 100f;
    Transform followTarget;
    Rigidbody handRigidbody;
    Collider[] colliders;

    void Start() {
        followTarget = followObject.transform;
        handRigidbody = GetComponent<Rigidbody>();
        colliders = GetComponentsInChildren<Collider>();

        handRigidbody.position = followTarget.position;
        handRigidbody.rotation = followTarget.rotation;
    }

    void Update() {
        var distance = Vector3.Distance(followTarget.position, transform.position);
        handRigidbody.velocity = (followTarget.position - transform.position).normalized * (followSpeed * distance);

        var q = followTarget.rotation * Quaternion.Inverse(handRigidbody.rotation);
        q.ToAngleAxis(out float angle, out Vector3 axis);
        handRigidbody.angularVelocity = axis * (angle * Mathf.Deg2Rad * rotateSpeed);
    }

    public void DisableColliders() {
        foreach (var collider in colliders) {
            collider.enabled = false;
        }
    }

    void EnableColliders() {
        foreach (var collider in colliders) {
            collider.enabled = true;
        }
    }

    public void EnableCollidersDelayed(float delay) {
        Invoke("EnableColliders", delay);
    }
}
