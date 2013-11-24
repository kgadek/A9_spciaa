/**
 * @author
 * @version 1.00 2011/6/13
 * @(#)Production.java
 */


abstract class Production extends Thread {

    Production(Vertex Vert, Counter Count) {
        m_vertex = Vert;
        m_counter = Count;
        m_counter.inc();
        m_drawer = new GraphDrawer();
    }

    //returns first vertex from the left
    abstract Vertex apply(Vertex v);

    //run the thread
    public void run() {
        m_vertex = apply(m_vertex);
        m_drawer.draw(m_vertex);
        m_counter.dec();
    }

    //vertex where the production will be applied
    Vertex m_vertex;
    //graph drawer
    GraphDrawer m_drawer;
    //productions counter
    Counter m_counter;
}

class P1 extends Production {
    P1(Vertex Vert, Counter Count) {
        super(Vert, Count);
    }

    Vertex apply(Vertex S) {
        System.out.println("p1");
        Vertex T1 = new Vertex(null, null, S, "T");
        Vertex T2 = new Vertex(null, null, S, "T");
        S.set_left(T1);
        S.set_right(T2);
        S.set_label("root");
        return S;
    }
}

class P2 extends Production {
    P2(Vertex Vert, Counter Count) {
        super(Vert, Count);
    }

    Vertex apply(Vertex T) {
        System.out.println("p2");
        Vertex T1 = new Vertex(null, null, T, "T");
        Vertex T2 = new Vertex(null, null, T, "T");
        T.set_left(T1);
        T.set_right(T2);
        T.set_label("int");
        return T;
    }
}

class P3 extends Production {
    P3(Vertex Vert, Counter Count) {
        super(Vert, Count);
    }

    Vertex apply(Vertex T) {
        System.out.println("p3");
        Vertex T1 = new Vertex(null, null, T, "node");
        Vertex T2 = new Vertex(null, null, T, "node");
        T.set_left(T1);
        T.set_right(T2);
        T.set_label("int");
        return T;
    }
}

class A1 extends Production {
    A1(Vertex Vert, Counter Count) {
        super(Vert, Count);
    }

    Vertex apply(Vertex T) {
        System.out.println("A1");
        T.m_a[1][1] = 1.0;
        T.m_a[2][1] = 1.0;
        T.m_a[1][2] = 0.0;
        T.m_a[2][2] = -1.0;
        T.m_b[1] = 0.0;
        T.m_b[2] = 0.0;

        return T;
    }
}

class A2 extends Production {
    A2(Vertex Vert, Counter Count) {
        super(Vert, Count);
    }

    Vertex apply(Vertex T) {
        System.out.println("A2");
        T.m_a[0][0] = T.m_left.m_a[2][2] + T.m_right.m_a[1][1];
        T.m_a[1][0] = T.m_left.m_a[1][2];
        T.m_a[2][0] = T.m_right.m_a[2][1];
        T.m_a[0][1] = T.m_left.m_a[2][1];
        T.m_a[1][1] = T.m_left.m_a[1][1];
        T.m_a[2][1] = 0.0;
        T.m_a[0][2] = T.m_right.m_a[1][2];
        T.m_a[1][2] = 0.0;
        T.m_a[2][2] = T.m_right.m_a[2][2];
        T.m_b[0] = 0.0;
        T.m_b[1] = 0.0;
        T.m_b[2] = 0.0;

        return T;
    }
}
