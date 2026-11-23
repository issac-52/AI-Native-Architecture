package lab.ddd.order.domain;
import java.util.List;
import java.util.Optional;
public interface OrderRepository {
    OrderAggregate create(String productName,int quantity);
    Optional<OrderAggregate> findById(long id);
    List<OrderAggregate> findAll();
}
