/**
 * @author
 * @version 1.00 2011/6/13
 * @(#)Executor.java
 */


class Executor extends Thread {
    public synchronized void run() {

        Counter counter = new Counter();
        //axiom
        Vertex S = new Vertex(null, null, null, "S");

        //p1
        P1 p1 = new P1(S, counter);
        p1.start();

        counter.release();

        //p2a,p2b
        P2 p2a = new P2(p1.m_vertex.m_left, counter);
        P2 p2b = new P2(p1.m_vertex.m_right, counter);
        p2a.start();
        p2b.start();

        counter.release();

        //p2^2,p3^2
        P2 p2c = new P2(p2a.m_vertex.m_left, counter);
        P2 p2d = new P2(p2a.m_vertex.m_right, counter);
        P3 p3a = new P3(p2b.m_vertex.m_left, counter);
        P3 p3b = new P3(p2b.m_vertex.m_right, counter);
        p2c.start();
        p2d.start();
        p3a.start();
        p3b.start();

        counter.release();

        //p3^4
        P3 p3c = new P3(p2c.m_vertex.m_left, counter);
        P3 p3d = new P3(p2c.m_vertex.m_right, counter);
        P3 p3e = new P3(p2d.m_vertex.m_left, counter);
        P3 p3f = new P3(p2d.m_vertex.m_right, counter);
        p3c.start();
        p3d.start();
        p3e.start();
        p3f.start();

        counter.release();

        //done
        System.out.println("done");
        GraphDrawer drawer = new GraphDrawer();
        drawer.draw(p1.m_vertex);

    }
}

/*
class Executor extends Thread {
	public synchronized void run() {

	  	Counter counter = new Counter(this);
		//axiom
		Vertex S = new Vertex(null,null,null,"S");

		//p1
		P1 p1 = new P1(S,counter);
		p1.start();

		counter.release();

		//p2
		P2 p2a = new P2(p1.m_vertex.m_left,counter);
		p2a.start();

		counter.release();

		//p2
		P2 p2b = new P2(p1.m_vertex.m_right,counter);
		p2b.start();

		counter.release();

		//p2
		P2 p2c = new P2(p2a.m_vertex.m_left,counter);
		p2c.start();

		counter.release();

		//p2
		P2 p2d = new P2(p2a.m_vertex.m_right,counter);
		p2d.start();

		counter.release();

		//p3
		P3 p3a = new P3(p2b.m_vertex.m_left,counter);
		p3a.start();

		counter.release();

		//p3
		P3 p3b = new P3(p2b.m_vertex.m_right,counter);
		p3b.start();

		counter.release();

		//p3
		P3 p3c = new P3(p2c.m_vertex.m_left,counter);
		p3c.start();

		counter.release();

		//p3
		P3 p3d = new P3(p2c.m_vertex.m_right,counter);
		p3d.start();

		counter.release();

		//p3
		P3 p3e = new P3(p2d.m_vertex.m_left,counter);
		p3e.start();

		counter.release();

		//p3
		P3 p3f = new P3(p2d.m_vertex.m_right,counter);
		p3f.start();

		counter.release();

		//done
		System.out.println("done");
		GraphDrawer drawer = new GraphDrawer();
		drawer.draw(p1.m_vertex);
	}
}
*/
