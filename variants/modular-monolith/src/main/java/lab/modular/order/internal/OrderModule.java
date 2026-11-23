package lab.modular.order.internal;
import lab.modular.order.api.OrderFacade;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;
@Service
class OrderModule implements OrderFacade {
    private final OrderMemory memory;
    OrderModule(OrderMemory memory){this.memory=memory;}
    private OrderView view(OrderEntity x){return new OrderView(x.id,x.productName,x.quantity,x.getStatus());}
    public OrderView create(String name,Integer qty){
        if(name==null || name.isBlank() || qty==null || qty<1)
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"Invalid order");
        return view(memory.insert(name.trim(),qty));
    }
    public List<OrderView> list(){return memory.all().stream().map(this::view).toList();}
    public OrderView cancel(long id){
        OrderEntity x=memory.get(id);
        if(x==null) throw new ResponseStatusException(HttpStatus.NOT_FOUND,"Order not found");
        x.cancel(); return view(x);
    }
}
