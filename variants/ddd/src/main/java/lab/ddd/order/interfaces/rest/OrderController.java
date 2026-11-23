package lab.ddd.order.interfaces.rest;
import lab.ddd.order.application.OrderApplicationService;
import lab.ddd.order.domain.OrderAggregate;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
@RestController
@RequestMapping("/api/orders")
public class OrderController {
    private final OrderApplicationService service;
    public OrderController(OrderApplicationService service){this.service=service;}
    public record Request(String productName,Integer quantity){}
    @PostMapping @ResponseStatus(HttpStatus.CREATED)
    public OrderAggregate create(@RequestBody Request req){
        return service.create(req.productName(),req.quantity());
    }
    @GetMapping public List<OrderAggregate> list(){return service.list();}
    @PostMapping("/{id}/cancel")
    public OrderAggregate cancel(@PathVariable long id){return service.cancel(id);}
}
