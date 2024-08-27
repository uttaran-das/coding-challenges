package test;

import main.HuffmanDeserializer;
import main.HuffmanNode;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class HuffmanDeserializerTest {

    @Test
    public void testDeserializeTree() {
        // Arrange
        String serializedTree = "001a1b01c1d";

        // Act
        HuffmanNode root = HuffmanDeserializer.deserializeTree(serializedTree);

        // Assert
        // Check the root node
        assertEquals(0, root.frequency);
        assertNotNull(root.left);
        assertNotNull(root.right);

        // Check the left subtree
        HuffmanNode left = root.left;
        assertEquals(0, left.frequency);
        assertNotNull(root.left);
        assertNotNull(left.right);

        HuffmanNode leftLeft = left.left;
        assertEquals('a', leftLeft.character);
        assertTrue(leftLeft.isLeaf());

        HuffmanNode leftRight = left.right;
        assertEquals('b', leftRight.character);
        assertTrue(leftRight.isLeaf());

        // Check the right subtree
        HuffmanNode right = root.right;
        assertEquals(0, right.frequency);
        assertNotNull(right.left);
        assertNotNull(right.right);

        HuffmanNode rightLeft = right.left;
        assertEquals('c', rightLeft.character);
        assertTrue(rightLeft.isLeaf());

        HuffmanNode rightRight = right.right;
        assertEquals('d', rightRight.character);
        assertTrue(rightRight.isLeaf());
    }
}