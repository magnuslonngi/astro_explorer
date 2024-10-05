using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.XR;

[RequireComponent(typeof(Animator))]
public class HandAnimator : MonoBehaviour {
    [SerializeField] UnityEngine.XR.InputDevice device;
    [SerializeField] InputActionProperty trigger;
    [SerializeField] InputActionProperty grip;
    InputFeatureUsage<bool> primary2DAxisTouch = new InputFeatureUsage<bool>("Primary2DAxisTouch");

    Animator animator;

    void Start() {
        animator = GetComponent<Animator>();
    }

    void Update() {
        float triggerValue = trigger.action.ReadValue<float>();
        float gripValue = grip.action.ReadValue<float>();

        if (device.TryGetFeatureValue(primary2DAxisTouch, out bool isThumbstickTouched)) {
            animator.SetBool("Thumb", isThumbstickTouched);
        }

        animator.SetFloat("Trigger", triggerValue);
        animator.SetFloat("Grip", gripValue);
    }
}
