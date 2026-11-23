package lab.hexagonal.adapter.out.memory;
import lab.hexagonal.application.port.out.OrderPersistencePort;
import lab.hexagonal.domain.Order;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicLong;
import org.springframework.stereotype.Repository;
@Repository
public class InMemoryOrderAdapter implements OrderPersistencePort {
    private final AtomicLong next=new AtomicLong();
    private final ConcurrentHashMap<Long,Order> orders=new ConcurrentHashMap<>();
    public Order create(String name,int qty){
        Order item=new Order(next.incrementAndGet(),name,qty);
        orders.put(item.getId(),item); return item;
    }
    public Optional<Order> find(long id){return Optional.ofNullable(orders.get(id));}
    public List<Order> findAll(){
        return orders.values().stream().sorted(Comparator.comparingLong(Order::getId)).toList();
    }
}
