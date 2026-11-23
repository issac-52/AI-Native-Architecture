package lab.hexagonal.application.service;
import lab.hexagonal.domain.Order;
import lab.hexagonal.application.port.in.OrderUseCases;
import lab.hexagonal.application.port.out.OrderPersistencePort;
import java.util.List;
import java.util.NoSuchElementException;
/** Framework-free application service depends only on ports and domain. */
public class OrderService implements OrderUseCases {
    private final OrderPersistencePort storage;
    public OrderService(OrderPersistencePort storage){this.storage=storage;}
    public Order create(String name,Integer qty){
        if(name==null || name.isBlank() || qty==null || qty<1)
            throw new IllegalArgumentException("Invalid order");
        return storage.create(name.trim(),qty);
    }
    public List<Order> list(){return storage.findAll();}
    public Order cancel(long id){
        Order item=storage.find(id).orElseThrow(()->new NoSuchElementException("Order not found"));
        item.cancel(); return item;
    }
}
