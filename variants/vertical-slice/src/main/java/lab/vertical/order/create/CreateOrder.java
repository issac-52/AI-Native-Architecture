package lab.vertical.order.create;
import lab.vertical.order.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.http.HttpStatus;
@RestController
@RequestMapping("/api/orders")
public class CreateOrder {
    private final OrderMemory memory;
    public CreateOrder(OrderMemory memory){this.memory=memory;}
    public record Request(String productName, Integer quantity){}
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Order create(@RequestBody Request request){
        if(request.productName()==null || request.productName().isBlank()
                || request.quantity()==null || request.quantity()<1)
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"Invalid order");
        return memory.create(request.productName().trim(),request.quantity());
    }
}
