package lab.hexagonal.application.port.out;
import lab.hexagonal.domain.Order;
import java.util.*;
public interface OrderPersistencePort {
    Order create(String name,int quantity);
    Optional<Order> find(long id);
    List<Order> findAll();
}
