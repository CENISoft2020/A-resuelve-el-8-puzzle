import javax.swing.*;
import javax.swing.tree.DefaultMutableTreeNode;
import java.awt.*;
import java.util.List;

public class PuzzleTreePanel extends JPanel {

    public PuzzleTreePanel(List<int[][]> path) {
        setLayout(new BorderLayout());

        // Crear el nodo raíz con el estado inicial
        DefaultMutableTreeNode root = new DefaultMutableTreeNode("Inicio");
        buildTree(root, path, 0);

        // Crear el JTree con la raíz
        JTree tree = new JTree(root);
        JScrollPane scrollPane = new JScrollPane(tree);

        // Agregar el JTree al panel
        add(scrollPane, BorderLayout.CENTER);
    }

    // Método recursivo para construir el árbol
    private void buildTree(DefaultMutableTreeNode node, List<int[][]> path, int index) {
        if (index >= path.size()) return;

        int[][] state = path.get(index);
        StringBuilder sb = new StringBuilder();
        for (int[] row : state) {
            sb.append("<html>");
            for (int val : row) {
                sb.append(val).append(" ");
            }
            sb.append("<br>");
        }
        sb.append("</html>");

        DefaultMutableTreeNode childNode = new DefaultMutableTreeNode(sb.toString());
        node.add(childNode);

        // Llamada recursiva para el siguiente estado
        buildTree(childNode, path, index + 1);
    }

    public static void createAndShowGUI(List<int[][]> path) {
        JFrame frame = new JFrame("Árbol de Solución del Puzzle");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.add(new PuzzleTreePanel(path));
        frame.setSize(400, 600);
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);
    }

    public static void main(String[] args) {
        // Ejemplo de estados en el camino
        List<int[][]> examplePath = List.of(
                new int[][]{{1, 2, 3}, {4, 0, 5}, {6, 7, 8}},
                new int[][]{{1, 2, 3}, {4, 7, 5}, {6, 0, 8}},
                new int[][]{{1, 2, 3}, {4, 7, 5}, {6, 8, 0}},
                new int[][]{{1, 2, 3}, {4, 7, 0}, {6, 8, 5}},
                new int[][]{{1, 2, 3}, {4, 0, 7}, {6, 8, 5}},
                new int[][]{{1, 2, 3}, {0, 4, 7}, {6, 8, 5}},
                new int[][]{{1, 0, 3}, {4, 2, 7}, {6, 8, 5}}
        );

        SwingUtilities.invokeLater(() -> createAndShowGUI(examplePath));
    }
}
