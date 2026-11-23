package lab.vertical.order.list;
import lab.vertical.order.*;
import java.util.List;
import org.springframework.web.bind.annotation.*;
@RestController
@RequestMapping("/api/orders")
public class ListOrders {
    private final OrderMemory memory;
    public ListOrders(OrderMemory memory){this.memory=memory;}
    @GetMapping
    public List<Order> list(){return memory.list();}
}
