/**
 * @author
 * @version 1.00 2011/6/13
 * @(#)Counter.java
 */


class Counter {
    int m_counter;

    synchronized void inc() {
        m_counter++;
    }

    synchronized void dec() {
        if (m_counter > 0)
            m_counter--;
        if (m_counter == 0)
            notifyAll();
    }

    synchronized void release() {
        while (m_counter > 0)
            try {
                wait();
            } catch (InterruptedException e) {
            }
    }
}
