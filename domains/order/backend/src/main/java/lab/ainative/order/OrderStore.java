package lab.ainative.order;

import java.util.Comparator;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

@Service
public class OrderStore {
    private final AtomicLong nextId = new AtomicLong();
    private final ConcurrentHashMap<Long, Order> orders = new ConcurrentHashMap<>();

    public List<Order> list() {
        return orders.values().stream().sorted(Comparator.comparingLong(Order::getId)).toList();
    }
    public Order create(String productName, Integer quantity) {
        if (productName == null || productName.isBlank() || quantity == null || quantity < 1) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "productName must be nonblank and quantity >= 1");
        }
        Order order = new Order(nextId.incrementAndGet(), productName.trim(), quantity);
        orders.put(order.getId(), order);
        return order;
    }
    public Order cancel(long id) {
        Order order = orders.get(id);
        if (order == null) throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Order not found");
        order.cancel(); // deliberately idempotent
        return order;
    }
}
