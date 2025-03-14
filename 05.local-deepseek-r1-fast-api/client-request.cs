/// <summary>
/// This script sends a prompt to a local API endpoint and processes the response.
/// It continuously prompts the user for input, sends the input to the API, and displays the response.
/// </summary>
/// <remarks>
/// The script uses HttpClient to send POST requests to the specified URL with a JSON payload.
/// The payload contains a model identifier and the user's prompt.
/// The response is expected to be in JSON format, and the script extracts and displays the response content.
/// </remarks>
/// <example>
/// To run this script, use the following command in the terminal:
/// <code>
/// dotnet run
/// </code>
/// After creating the console app project with the command in terminal:
/// <code>
/// dotnet new console
/// </code>
/// And remove the Program.cs, you might need to nuget install Newtonsoft.Json and System.Net.Http.Json
/// <code>
/// dotnet add package Newtonsoft.Json
/// dotnet add package System.Net.Http.Json
/// </code>
/// </example>
/// <dependencies>
/// - System
/// - System.Net.Http
/// - System.Text
/// - System.Threading.Tasks
/// - Newtonsoft.Json
/// </dependencies>
using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

string url = "http://127.0.0.1:11434/api/generate";
HttpClient client = new HttpClient
{
    Timeout = TimeSpan.FromMinutes(10) // Set timeout to 10 minutes
};

// client.DefaultRequestHeaders.Add("Content-Type", "application/json");

string qn = "As an expert in Godot 4.3 C#, please give me a lesson on how to create a simple 2D procedurally generated world using my own implemented seeded perlin noise instead of built in noise.";
Console.WriteLine("Q: " + qn);

while (!string.IsNullOrEmpty(qn))
{
    var payload = new
    {
        model = "deepseek-r1:8b",
        prompt = qn
    };

    Console.WriteLine("Sending request");
    var startTime = DateTime.Now;
    var content = new StringContent(JsonConvert.SerializeObject(payload), Encoding.UTF8, "application/json");
    var response = await client.PostAsync(url, content);
    var endTime = DateTime.Now;
    Console.WriteLine("Response received");
    Console.WriteLine($"Execution time: {(endTime - startTime).TotalSeconds} seconds");

    var responseText = await response.Content.ReadAsStringAsync();
    var rows = responseText.Split('\n');
    var answer = new StringBuilder();

    foreach (var row in rows)
    {
        try
        {
            var jsonRow = JsonConvert.DeserializeObject<dynamic>(row);
            if (jsonRow?.response != null)
            {
                answer.Append(jsonRow.response);
            }
        }
        catch
        {
            continue;
        }
    }

    Console.WriteLine(answer.ToString());
    Console.WriteLine();
    Console.Write("Q: ");
    qn = Console.ReadLine() ?? string.Empty;
}

Console.WriteLine("Bye!");