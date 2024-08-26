package main;

import java.util.Map;
import java.util.PriorityQueue;

public class HuffmanCoding {
    public static HuffmanNode buildHuffmanTree(Map<Character, Integer> frequencyMap) {
        PriorityQueue<HuffmanNode> pq = new PriorityQueue<>();
        for (Map.Entry<Character, Integer> entry: frequencyMap.entrySet()) {
            pq.add(new HuffmanNode(entry.getKey(), entry.getValue()));
        }

        while (pq.size() > 1) {
            HuffmanNode left = pq.poll();
            HuffmanNode right = pq.poll();
            HuffmanNode parent = new HuffmanNode(left.frequency + right.frequency, left, right);
            pq.add(parent);
        }

        return pq.poll();
    }

    public static String getHuffmanCode(HuffmanNode root, char character) {
        return getHuffmanCodeHelper(root, character, "");
    }

    private static String getHuffmanCodeHelper(HuffmanNode node, char character, String code) {
        if (node.isLeaf()) {
            return node.character == character ? code : null;
        }

        String leftCode = getHuffmanCodeHelper(node.left, character, code + "0");
        if (leftCode != null) {
            return leftCode;
        }

        return getHuffmanCodeHelper(node.right, character, code + "1");
    }
}
