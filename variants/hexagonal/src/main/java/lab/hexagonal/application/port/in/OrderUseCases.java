package lab.hexagonal.application.port.in;
import lab.hexagonal.domain.Order;
import java.util.List;
public interface OrderUseCases {
    Order create(String productName,Integer quantity);
    List<Order> list();
    Order cancel(long id);
}
