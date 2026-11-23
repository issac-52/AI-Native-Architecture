package lab.baseline.service;

import lab.baseline.model.Order;
import lab.baseline.repository.OrderRepository;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

@Service
public class OrderService {
    private final OrderRepository repository;
    public OrderService(OrderRepository repository) { this.repository = repository; }
    public List<Order> list() { return repository.findAll(); }
    public Order create(String productName, Integer quantity) {
        if (productName == null || productName.isBlank() || quantity == null || quantity < 1) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "productName must be nonblank and quantity >= 1");
        }
        return repository.save(productName.trim(), quantity);
    }
    public Order cancel(long id) {
        Order order = repository.findById(id);
        if (order == null) throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Order not found");
        order.cancel();
        return order;
    }
}
