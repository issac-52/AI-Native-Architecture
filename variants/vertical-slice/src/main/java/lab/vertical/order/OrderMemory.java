package lab.vertical.order;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicLong;
import org.springframework.stereotype.Repository;
@Repository
public class OrderMemory {
    private final AtomicLong next = new AtomicLong();
    private final ConcurrentHashMap<Long,Order> orders = new ConcurrentHashMap<>();
    public Order create(String name, int quantity) {
        Order item = new Order(next.incrementAndGet(), name, quantity);
        orders.put(item.getId(), item);
        return item;
    }
    public List<Order> list(){
        return orders.values().stream().sorted(Comparator.comparingLong(Order::getId)).toList();
    }
    public Order find(long id){return orders.get(id);}
}
