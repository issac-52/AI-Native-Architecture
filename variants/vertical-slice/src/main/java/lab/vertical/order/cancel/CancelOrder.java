package lab.vertical.order.cancel;
import lab.vertical.order.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.http.HttpStatus;
@RestController
@RequestMapping("/api/orders")
public class CancelOrder {
    private final OrderMemory memory;
    public CancelOrder(OrderMemory memory){this.memory=memory;}
    @PostMapping("/{id}/cancel")
    public Order cancel(@PathVariable long id) {
        Order item=memory.find(id);
        if(item==null) throw new ResponseStatusException(HttpStatus.NOT_FOUND,"Order not found");
        item.cancel();
        return item;
    }
}
