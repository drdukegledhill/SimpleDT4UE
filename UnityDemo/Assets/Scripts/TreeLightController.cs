using UnityEngine;

public class TreeLightController : MonoBehaviour
{
    public GameObject pixelPrefab; // Assign a sphere prefab in the inspector
    public GameObject starPrefab;  // Assign a star prefab in the inspector (optional)
    public TreeClient treeClient;
    public int columns = 8;
    public int rows = 3;
    public float spacing = 1.2f;
    public float starYOffset = 1.5f;

    private GameObject[] pixels = new GameObject[25];
    private int selectedPixel = -1;

    void Start()
    {
        GenerateTree();
    }

    void Update()
    {
        // Robust pixel selection using raycast
        if (Input.GetMouseButtonDown(0))
        {
            Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
            if (Physics.Raycast(ray, out RaycastHit hit))
            {
                var clicker = hit.collider.GetComponent<TreePixelClickHandler>();
                if (clicker != null)
                {
                    OnPixelSelected(clicker.pixelIndex);
                }
            }
        }
    }

    void GenerateTree()
    {
        // Place the star (pixel 3) at the top center
        Vector3 starPos = new Vector3((columns - 1) * spacing / 2, rows * spacing + starYOffset, 0);
        GameObject star = Instantiate(starPrefab != null ? starPrefab : pixelPrefab, starPos, Quaternion.identity, transform);
        star.name = "Star (Pixel 3)";
        pixels[3] = star;
        SetPixelColor(3, Color.white);
        AddPixelClickHandler(star, 3);

        // Place 8 columns of 3 pixels each
        int pixelIdx = 0;
        for (int col = 0; col < columns; col++)
        {
            for (int row = 0; row < rows; row++)
            {
                if (pixelIdx == 3) pixelIdx++; // Skip star index
                if (pixelIdx >= 25) break;
                float x = col * spacing;
                float y = (col % 2 == 0 ? row : (rows - 1 - row)) * spacing; // Even columns upside down
                Vector3 pos = new Vector3(x, y, 0);
                GameObject pixel = Instantiate(pixelPrefab, pos, Quaternion.identity, transform);
                pixel.name = $"Pixel {pixelIdx}";
                pixels[pixelIdx] = pixel;
                SetPixelColor(pixelIdx, Color.black);
                AddPixelClickHandler(pixel, pixelIdx);
                pixelIdx++;
            }
        }
    }

    void AddPixelClickHandler(GameObject pixel, int idx)
    {
        var collider = pixel.GetComponent<Collider>();
        if (collider == null) pixel.AddComponent<SphereCollider>();
        var clicker = pixel.AddComponent<TreePixelClickHandler>();
        clicker.controller = this;
        clicker.pixelIndex = idx;
    }

    public void OnPixelSelected(int idx)
    {
        selectedPixel = idx;
        // You can update UI here to show color/brightness controls for selected pixel
        Debug.Log($"Selected pixel {idx}");
    }

    public void SetPixelColor(int idx, Color color)
    {
        if (pixels[idx] != null)
        {
            var renderer = pixels[idx].GetComponent<Renderer>();
            if (renderer != null)
            {
                renderer.material.color = color;
            }
        }
        // Optionally send to server
        if (treeClient != null && treeClient.IsConnected)
        {
            treeClient.SetPixel(idx, color.r, color.g, color.b);
        }
    }

    public int GetSelectedPixel() => selectedPixel;
    public Color GetPixelColor(int idx)
    {
        if (pixels[idx] != null)
        {
            var renderer = pixels[idx].GetComponent<Renderer>();
            if (renderer != null)
            {
                return renderer.material.color;
            }
        }
        return Color.black;
    }
}

// Helper for click detection
public class TreePixelClickHandler : MonoBehaviour
{
    public TreeLightController controller;
    public int pixelIndex;
    // No OnMouseDown needed; selection is handled by TreeLightController's Update()
} 