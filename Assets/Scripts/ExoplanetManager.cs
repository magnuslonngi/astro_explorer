using TMPro;
using UnityEngine;

public class ExoplanetManager : MonoBehaviour {
    [SerializeField] ExoInfo exoInfo1;
    [SerializeField] ExoInfo exoInfo2;
    [SerializeField] ExoInfo exoInfo3;
    [SerializeField] ExoInfo exoInfo4;

    public void UpdateTables(Exoplanet exoplanet) {
        exoInfo1.firstValue.text = exoplanet.name;
        exoInfo1.secondValue.text = exoplanet.data.pl_orbper;

        exoInfo2.firstValue.text = exoplanet.data.discoverymethod;
        exoInfo2.secondValue.text = exoplanet.data.disc_year;

        exoInfo3.firstValue.text = exoplanet.data.disc_telescope;
        exoInfo3.secondValue.text = exoplanet.data.disc_pubdate;

        exoInfo4.firstValue.text = exoplanet.data.disc_facility;
        exoInfo4.firstValue.text = exoplanet.data.disc_instrument;
    }

    public void ChangeSkybox(string name) {
        Cubemap cubemapTexture = Resources.Load<Cubemap>("Exoplanets/" + name);
        Material skyboxMaterial = new Material(Shader.Find("Skybox/Cubemap"));

        skyboxMaterial.SetTexture("_Tex", cubemapTexture);
        RenderSettings.skybox = skyboxMaterial;
    }
}

[System.Serializable]
public class ExoInfo {
    public TextMeshProUGUI firstValue;
    public TextMeshProUGUI secondValue;
}

[System.Serializable]
public class ExoplanetData {
    public string pl_orbper;
    public string discoverymethod;
    public string disc_year;
    public string disc_pubdate;
    public string disc_facility;
    public string disc_telescope;
    public string disc_instrument;
}

[System.Serializable]
public class Exoplanet {
    public string name;
    public ExoplanetData data;
}

[System.Serializable]
public class ExoplanetCollection {
    public Exoplanet[] exoplanets;
}
