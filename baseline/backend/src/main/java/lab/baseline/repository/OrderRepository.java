package lab.baseline.repository;

import lab.baseline.model.Order;
import java.util.Comparator;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;
import org.springframework.stereotype.Repository;

@Repository
public class OrderRepository {
    private final AtomicLong nextId = new AtomicLong();
    private final ConcurrentHashMap<Long, Order> orders = new ConcurrentHashMap<>();

    public List<Order> findAll() {
        return orders.values().stream().sorted(Comparator.comparingLong(Order::getId)).toList();
    }
    public Order save(String productName, int quantity) {
        Order order = new Order(nextId.incrementAndGet(), productName, quantity);
        orders.put(order.getId(), order);
        return order;
    }
    public Order findById(long id) { return orders.get(id); }
}
