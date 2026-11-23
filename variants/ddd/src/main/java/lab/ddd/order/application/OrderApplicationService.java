package lab.ddd.order.application;
import lab.ddd.order.domain.*;
import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;
@Service
public class OrderApplicationService {
    private final OrderRepository repository;
    public OrderApplicationService(OrderRepository repository){this.repository=repository;}
    public OrderAggregate create(String name,Integer qty){
        if(name==null || name.isBlank() || qty==null || qty<1)
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"Invalid order");
        return repository.create(name.trim(),qty);
    }
    public List<OrderAggregate> list(){return repository.findAll();}
    public OrderAggregate cancel(long id){
        OrderAggregate item=repository.findById(id).orElseThrow(
            ()->new ResponseStatusException(HttpStatus.NOT_FOUND,"Order not found"));
        item.cancel(); return item;
    }
}
