import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class BackendServer {
    public static void main(String[] args) {
        int port = 8080;
        try (ServerSocket serverSocket = new ServerSocket(port)) {
            System.out.println("Backend server listening on port " + port + "...");

            while (true) {
                Socket clientSocket = serverSocket.accept();
                System.out.println("Received request from " + clientSocket.getInetAddress().getHostAddress());

                BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                String request = in.readLine();
                while (request != null && !request.isEmpty()) {
                    System.out.println(request);
                    request = in.readLine();
                }
                PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);
                String response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello From Backend Server";
                out.println(response);
                out.flush();
                System.out.println("Replied with a hello message");

                clientSocket.close();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}