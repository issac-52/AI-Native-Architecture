package lab.modular.web;
import lab.modular.order.api.OrderFacade;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
@RestController
@RequestMapping("/api/orders")
public class OrderController {
    private final OrderFacade orders;
    public OrderController(OrderFacade orders){this.orders=orders;}
    public record Request(String productName,Integer quantity){}
    @PostMapping @ResponseStatus(HttpStatus.CREATED)
    public OrderFacade.OrderView create(@RequestBody Request req){return orders.create(req.productName(),req.quantity());}
    @GetMapping public List<OrderFacade.OrderView> list(){return orders.list();}
    @PostMapping("/{id}/cancel")
    public OrderFacade.OrderView cancel(@PathVariable long id){return orders.cancel(id);}
}
