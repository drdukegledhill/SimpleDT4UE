using System;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;

public class TreeClient : MonoBehaviour
{
    public string host = "192.168.178.195";
    public int port = 65436;
    public bool IsConnected { get; private set; } = false;

    private TcpClient client;
    private NetworkStream stream;
    private Thread clientThread;
    private bool running = false;

    public void Connect()
    {
        if (IsConnected) return;
        running = true;
        clientThread = new Thread(ClientThreadFunc);
        clientThread.IsBackground = true;
        clientThread.Start();
    }

    public void Disconnect()
    {
        running = false;
        if (stream != null) stream.Close();
        if (client != null) client.Close();
        IsConnected = false;
    }

    private void ClientThreadFunc()
    {
        try
        {
            client = new TcpClient();
            client.Connect(host, port);
            stream = client.GetStream();
            IsConnected = true;
            Debug.Log($"[TreeClient] Connected to {host}:{port}");
            // Optionally, listen for server responses here
        }
        catch (Exception e)
        {
            Debug.LogError($"[TreeClient] Connection error: {e.Message}");
            IsConnected = false;
        }
    }

    public void SendCommand(string json)
    {
        if (!IsConnected || stream == null) return;
        try
        {
            byte[] data = Encoding.UTF8.GetBytes(json);
            stream.Write(data, 0, data.Length);
            Debug.Log($"[TreeClient] Sent: {json}");
        }
        catch (Exception e)
        {
            Debug.LogError($"[TreeClient] Send error: {e.Message}");
        }
    }

    public void SetPixel(int pixel, float r, float g, float b)
    {
        string json = $"{{\"type\":\"set_pixel\",\"pixel\":{pixel},\"color\":[{r},{g},{b}]}}";
        SendCommand(json);
    }

    public void SetAll(float r, float g, float b)
    {
        string json = $"{{\"type\":\"set_all\",\"color\":[{r},{g},{b}]}}";
        SendCommand(json);
    }

    public void Off()
    {
        string json = "{\"type\":\"off\"}";
        SendCommand(json);
    }

    private void OnDestroy()
    {
        Disconnect();
    }
} 