import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.List;

public class LoadBalancer {
    private static final List<String> backendServers = new ArrayList<>();
    private static int currentServerIndex = 0;

    static {
        backendServers.add("localhost:8080");
        backendServers.add("localhost:8081");
    }

    public static void main(String[] args) {
        int port = 80;
        try (ServerSocket serverSocket = new ServerSocket(port)) {
            System.out.println("Load balancer listening on port " + port + "...");
            while (true) {
                Socket clientSocket = serverSocket.accept();
                new Thread(new ClientHandler(clientSocket)).start();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    static synchronized String getBackendServer() {
        String backendServer = backendServers.get(currentServerIndex);
        currentServerIndex = (currentServerIndex + 1) % backendServers.size();
        return backendServer;
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