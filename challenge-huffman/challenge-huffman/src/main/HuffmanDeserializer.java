package main;

public class HuffmanDeserializer {

    public static HuffmanNode deserializeTree(String serializedTree) {
        return deserializeTreeHelper(new StringBuilder(serializedTree));
    }

    private static HuffmanNode deserializeTreeHelper(StringBuilder sb) {
        if (sb.isEmpty()) {
            return null;
        }

        char type = sb.charAt(0);
        sb.deleteCharAt(0);

        if (type == '1') {
            // Leaf node
            char character = sb.charAt(0);
            sb.deleteCharAt(0);
            return new HuffmanNode(character, 0);
        } else {
            // Internal node
            HuffmanNode left = deserializeTreeHelper(sb);
            HuffmanNode right = deserializeTreeHelper(sb);
            return new HuffmanNode(0, left, right);
        }
    }
}