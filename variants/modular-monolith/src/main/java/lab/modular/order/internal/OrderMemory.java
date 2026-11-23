package lab.modular.order.internal;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicLong;
import org.springframework.stereotype.Repository;
@Repository
class OrderMemory {
    private final AtomicLong next = new AtomicLong();
    private final ConcurrentHashMap<Long,OrderEntity> items=new ConcurrentHashMap<>();
    OrderEntity insert(String name,int qty){
        OrderEntity order=new OrderEntity(next.incrementAndGet(),name,qty);
        items.put(order.id,order); return order;
    }
    OrderEntity get(long id){return items.get(id);}
    List<OrderEntity> all(){
        return items.values().stream().sorted(Comparator.comparingLong(x->x.id)).toList();
    }
}
