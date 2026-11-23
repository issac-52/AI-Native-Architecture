package lab.ainative.order;

import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/orders")
public class OrderController {
    private final OrderStore store;
    public OrderController(OrderStore store) { this.store = store; }

    public record CreateOrderRequest(String productName, Integer quantity) {}

    @GetMapping
    public List<Order> list() { return store.list(); }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Order create(@RequestBody CreateOrderRequest request) {
        return store.create(request.productName(), request.quantity());
    }

    @PostMapping("/{id}/cancel")
    public Order cancel(@PathVariable long id) { return store.cancel(id); }
}
