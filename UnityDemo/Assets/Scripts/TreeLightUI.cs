using UnityEngine;
using UnityEngine.UI;

public class TreeLightUI : MonoBehaviour
{
    public TreeLightController treeController;
    public TreeClient treeClient;
    public Button connectButton;
    public Button disconnectButton;
    public Button demoButton;
    public Button stopDemoButton;
    public Button offSelectedButton;
    public Button offAllButton;
    public Slider rSlider;
    public Slider gSlider;
    public Slider bSlider;
    public Slider brightnessSlider;
    public Text statusText;
    public Text selectedPixelText;

    private bool demoRunning = false;
    private bool stopDemoRequested = false;

    void Start()
    {
        connectButton.onClick.AddListener(() => treeClient.Connect());
        disconnectButton.onClick.AddListener(() => treeClient.Disconnect());
        demoButton.onClick.AddListener(RunDemo);
        stopDemoButton.onClick.AddListener(() => stopDemoRequested = true);
        offSelectedButton.onClick.AddListener(OffSelected);
        offAllButton.onClick.AddListener(OffAll);
        rSlider.onValueChanged.AddListener(_ => UpdateSelectedPixelColor());
        gSlider.onValueChanged.AddListener(_ => UpdateSelectedPixelColor());
        bSlider.onValueChanged.AddListener(_ => UpdateSelectedPixelColor());
        brightnessSlider.onValueChanged.AddListener(_ => UpdateSelectedPixelColor());
        UpdateUI();
    }

    void Update()
    {
        UpdateUI();
    }

    void UpdateUI()
    {
        statusText.text = treeClient.IsConnected ? "Connected" : "Disconnected";
        statusText.color = treeClient.IsConnected ? Color.green : Color.red;
        int sel = treeController.GetSelectedPixel();
        selectedPixelText.text = sel >= 0 ? $"Selected: {sel}" : "No pixel selected";
        bool pixelSelected = sel >= 0;
        rSlider.interactable = pixelSelected;
        gSlider.interactable = pixelSelected;
        bSlider.interactable = pixelSelected;
        brightnessSlider.interactable = pixelSelected;
        offSelectedButton.interactable = pixelSelected;
        if (pixelSelected)
        {
            Color c = treeController.GetPixelColor(sel);
            float brightness = Mathf.Max(c.r, c.g, c.b);
            if (brightness > 0)
            {
                rSlider.value = c.r / brightness;
                gSlider.value = c.g / brightness;
                bSlider.value = c.b / brightness;
                brightnessSlider.value = brightness;
            }
            else
            {
                rSlider.value = 1;
                gSlider.value = 1;
                bSlider.value = 1;
                brightnessSlider.value = 1;
            }
        }
    }

    void UpdateSelectedPixelColor()
    {
        int sel = treeController.GetSelectedPixel();
        if (sel < 0) return;
        float r = rSlider.value * brightnessSlider.value;
        float g = gSlider.value * brightnessSlider.value;
        float b = bSlider.value * brightnessSlider.value;
        treeController.SetPixelColor(sel, new Color(r, g, b));
    }

    void OffSelected()
    {
        int sel = treeController.GetSelectedPixel();
        if (sel >= 0)
        {
            treeController.SetPixelColor(sel, Color.black);
        }
    }

    void OffAll()
    {
        for (int i = 0; i < 25; i++)
        {
            treeController.SetPixelColor(i, Color.black);
        }
        treeClient.Off();
    }

    void RunDemo()
    {
        if (demoRunning) return;
        demoRunning = true;
        stopDemoRequested = false;
        demoButton.interactable = false;
        stopDemoButton.interactable = true;
        StartCoroutine(DemoCoroutine());
    }

    System.Collections.IEnumerator DemoCoroutine()
    {
        // Color wipes: red, green, blue
        Color[] colors = { Color.red, Color.green, Color.blue };
        foreach (var color in colors)
        {
            for (int i = 0; i < 25; i++)
            {
                if (stopDemoRequested) { FinishDemo(); yield break; }
                treeController.SetPixelColor(i, color);
                yield return new WaitForSeconds(0.1f);
            }
            yield return new WaitForSeconds(0.5f);
        }
        // Static rainbow
        for (int i = 0; i < 25; i++)
        {
            if (stopDemoRequested) { FinishDemo(); yield break; }
            float hue = i / 25f;
            Color rgb = Color.HSVToRGB(hue, 1f, 1f);
            treeController.SetPixelColor(i, rgb);
        }
        yield return new WaitForSeconds(2f);
        // Sparkle effect
        for (int j = 0; j < 50; j++)
        {
            if (stopDemoRequested) { FinishDemo(); yield break; }
            int pixel = Random.Range(0, 25);
            Color color = new Color(Random.value, Random.value, Random.value);
            treeController.SetPixelColor(pixel, color);
            yield return new WaitForSeconds(0.1f);
        }
        OffAll();
        FinishDemo();
    }

    void FinishDemo()
    {
        demoRunning = false;
        stopDemoRequested = false;
        demoButton.interactable = true;
        stopDemoButton.interactable = false;
    }
} 