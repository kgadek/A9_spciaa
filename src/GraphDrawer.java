/**
 * @author
 * @version 1.00 2011/6/13
 * @(#)GraphDrawer.java
 */


class GraphDrawer {
    GraphDrawer() {
    }

    //draw the graph
    void draw(Vertex v) {
        //plot the tree in the pre-order
        //go up to the root
        while (v.m_parent != null) {
            v = v.m_parent;
        }
        //plot
        plot_preorder(v, 0);
        System.out.println();
    }

    void plot_preorder(Vertex v, int shift) {
        if(v == null) {
            System.out.print("null");
            return;
        }
        int newShift = shift + 2 + v.m_label.length();

        System.out.format("(%s ", v.m_label);
        plot_preorder(v.m_left, newShift);
        System.out.format("\n%" + newShift + "s", " ");
        plot_preorder(v.m_right, newShift);
        System.out.print(")");
    }
}
