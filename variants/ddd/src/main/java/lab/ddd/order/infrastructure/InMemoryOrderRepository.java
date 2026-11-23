package lab.ddd.order.infrastructure;
import lab.ddd.order.domain.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicLong;
import org.springframework.stereotype.Repository;
@Repository
public class InMemoryOrderRepository implements OrderRepository {
    private final AtomicLong next = new AtomicLong();
    private final ConcurrentHashMap<Long, OrderAggregate> orders = new ConcurrentHashMap<>();
    public OrderAggregate create(String name,int quantity){
        OrderAggregate item=new OrderAggregate(next.incrementAndGet(),name,quantity);
        orders.put(item.getId(),item); return item;
    }
    public Optional<OrderAggregate> findById(long id){return Optional.ofNullable(orders.get(id));}
    public List<OrderAggregate> findAll(){
        return orders.values().stream().sorted(Comparator.comparingLong(OrderAggregate::getId)).toList();
    }
}
