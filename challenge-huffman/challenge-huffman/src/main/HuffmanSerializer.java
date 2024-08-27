package main;

public class HuffmanSerializer {

    public static String serializeTree(HuffmanNode root) {
        StringBuilder sb = new StringBuilder();
        serializeTreeHelper(root, sb);
        return sb.toString();
    }

    private static void serializeTreeHelper(HuffmanNode node, StringBuilder sb) {
        if (node == null) {
            return;
        }

        if (node.left == null && node.right == null) {
            // Leaf node
            sb.append("1").append(node.character);
        } else {
            // Internal node
            sb.append("0");
        }

        serializeTreeHelper(node.left, sb);
        serializeTreeHelper(node.right, sb);
    }
}