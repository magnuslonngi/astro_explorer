using UnityEngine.UI;
using UnityEngine;
using TMPro;
using System;

public class ExoplanetSelector : MonoBehaviour {
    [SerializeField] ExoplanetManager exoplanetManager;
    [SerializeField] GameObject exoplanetPrefab;
    [SerializeField] Transform exoplanetParent;
    GameObject lastSelected;
    Exoplanet currentExoplanet;

    void Start() {
        TextAsset jsonText = Resources.Load<TextAsset>("planet_data");
        ExoplanetCollection exoplanetCollection = JsonUtility.FromJson<ExoplanetCollection>(jsonText.text); 

        foreach (Exoplanet exoplanet in exoplanetCollection.exoplanets) {
            Debug.Log(exoplanet.name);
            GameObject newExoplanet = Instantiate(exoplanetPrefab, exoplanetParent.transform);
            newExoplanet.GetComponent<Button>().onClick.AddListener(() => SelectExoplanet(newExoplanet, exoplanet));
            newExoplanet.GetComponentInChildren<TextMeshProUGUI>().text = exoplanet.name;
        }
    }
    
    public void SelectExoplanet(GameObject selected, Exoplanet exoplanet) {
        if (lastSelected != null) {
            Image imageComponent = lastSelected.GetComponent<Image>();
            Color currentColor = imageComponent.color;
            currentColor.a = 0;
            imageComponent.color = currentColor;
        }

        Image selectedImage = selected.GetComponent<Image>();
        Color selectedColor = selectedImage.color;
        selectedColor.a = 1;
        selectedImage.color = selectedColor;
        currentExoplanet = exoplanet;

        lastSelected = selected;
    }

    public void TravelToExoplanet() {
        string text = lastSelected.GetComponentInChildren<TextMeshProUGUI>().text;
        var newText = text.Replace(" ", "_") + "_cv2_csc_out";
        exoplanetManager.ChangeSkybox(newText);
        exoplanetManager.UpdateTables(currentExoplanet);
    }
}
