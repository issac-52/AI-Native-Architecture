package lab.hexagonal.adapter.in.http;
import lab.hexagonal.application.port.in.OrderUseCases;
import lab.hexagonal.domain.Order;
import java.util.List;
import java.util.NoSuchElementException;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
@RestController
@RequestMapping("/api/orders")
public class OrderController {
    private final OrderUseCases cases;
    public OrderController(OrderUseCases cases){this.cases=cases;}
    public record Request(String productName,Integer quantity){}
    @PostMapping @ResponseStatus(HttpStatus.CREATED)
    public Order create(@RequestBody Request req){return cases.create(req.productName(),req.quantity());}
    @GetMapping public List<Order> list(){return cases.list();}
    @PostMapping("/{id}/cancel")
    public Order cancel(@PathVariable long id){return cases.cancel(id);}
    @ExceptionHandler(IllegalArgumentException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public String invalid(IllegalArgumentException ex){return ex.getMessage();}
    @ExceptionHandler(NoSuchElementException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public String missing(NoSuchElementException ex){return ex.getMessage();}
}
