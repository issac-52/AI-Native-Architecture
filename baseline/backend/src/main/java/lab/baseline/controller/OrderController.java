package lab.baseline.controller;

import lab.baseline.model.Order;
import lab.baseline.service.OrderService;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/orders")
public class OrderController {
    private final OrderService service;
    public OrderController(OrderService service) { this.service = service; }
    public record CreateOrderRequest(String productName, Integer quantity) {}

    @GetMapping
    public List<Order> list() { return service.list(); }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Order create(@RequestBody CreateOrderRequest request) {
        return service.create(request.productName(), request.quantity());
    }

    @PostMapping("/{id}/cancel")
    public Order cancel(@PathVariable long id) { return service.cancel(id); }
}
