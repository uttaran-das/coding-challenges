import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.HttpURLConnection;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.URI;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class LoadBalancer {
    private static final List<String> backendServers = new ArrayList<>();
    private static final List<String> availableServers = new ArrayList<>();
    private static int currentServerIndex = 0;
    private static final ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);

    static {
        backendServers.add("localhost:8080");
        backendServers.add("localhost:8081");
        backendServers.add("localhost:8082");
        availableServers.addAll(backendServers);
    }

    public static void main(String[] args) {
        if (args.length < 2){
            System.out.println("Usage: java LoadBalancer <healthCheckPeriod> <healthCheckURL>");
            return;
        }

        int healthCheckPeriod = Integer.parseInt(args[0]);
        String healthCheckURL = args[1];

        int port = 80;
        try (ServerSocket serverSocket = new ServerSocket(port)) {
            System.out.println("Load balancer listening on port " + port + "...");
            startHealthCheck(healthCheckPeriod, healthCheckURL);
            while (true) {
                Socket clientSocket = serverSocket.accept();
                new Thread(new ClientHandler(clientSocket)).start();
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            scheduler.shutdown();
        }
    }

    static synchronized String getBackendServer() {
        if (availableServers.isEmpty()) {
            throw new RuntimeException("No available backend servers");
        }
        currentServerIndex %= availableServers.size();
        String backendServer = availableServers.get(currentServerIndex);
        currentServerIndex++;
        return backendServer;
    }

    private static void startHealthCheck(int period, String healthCheckURL) {
        scheduler.scheduleAtFixedRate(() -> {
            for (String server : backendServers) {
                if (!performHealthCheck(server, healthCheckURL)) {
                    if (availableServers.contains(server)) {
                        availableServers.remove(server);
                        System.out.println("Backend server " + server + " is down. Marking it as unavailable.");
                    }
                } else {
                    if(!availableServers.contains(server)) {
                        availableServers.add(server);
                        System.out.println("Backend server " + server + " is up. Marking it as available.");
                    }
                }
            }
        }, 0, period, TimeUnit.SECONDS);
    }

    private static boolean performHealthCheck(String server, String healthCheckURL) {
        try {
            String[] parts = server.split(":");
            String host = parts[0];
            int port = Integer.parseInt(parts[1]);
            URL url = new URI("http", null, host, port, healthCheckURL, null, null).toURL();
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");
            int responseCode = connection.getResponseCode();
            return responseCode == 200;
        } catch (Exception e) {
            return false;
        }
    }
}

class ClientHandler implements Runnable {
    private Socket clientSocket;
    public ClientHandler(Socket clientSocket) {
        this.clientSocket = clientSocket;
    }

    @Override
    public void run() {
        try {
            System.out.println("Received request from " + clientSocket.getInetAddress().getHostAddress());

            // Read the request from the client
            BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
            StringBuilder requestBuilder = new StringBuilder();
            String requestLine;
            while ((requestLine = in.readLine()) != null && !requestLine.isEmpty()) {
                System.out.println(requestLine);
                requestBuilder.append(requestLine).append("\r\n");
            }

            // Get the backend server using round-robin algorithm
            String backendServer = LoadBalancer.getBackendServer();
            String[] backendServerParts = backendServer.split(":");
            String backendHost = backendServerParts[0];
            int backendPort = Integer.parseInt(backendServerParts[1]);

            // Forward the request to the backend server
            Socket backendSocket = new Socket(backendHost, backendPort);
            PrintWriter backendOut = new PrintWriter(backendSocket.getOutputStream(), true);
            backendOut.println(requestBuilder.toString());
            backendOut.flush();

            // Read the response from the backend server
            BufferedReader backendIn = new BufferedReader(new InputStreamReader(backendSocket.getInputStream()));
            StringBuilder responseBuilder = new StringBuilder();
            String responseLine;
            while ((responseLine = backendIn.readLine()) != null) { // We can't check for empty line here, otherwise later part of \r\n\r\n will not be read
                System.out.println(responseLine);
                responseBuilder.append(responseLine).append("\r\n");
            }

            // Send the response back to the client
            PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);
            out.println(responseBuilder.toString());
            out.flush();

            // Close the connections
            clientSocket.close();
            backendSocket.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}