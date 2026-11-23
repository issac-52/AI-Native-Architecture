package lab.modular.order.api;
import java.util.List;
/** Public module boundary: external code must not import order.internal. */
public interface OrderFacade {
    record OrderView(long id,String productName,int quantity,String status){}
    OrderView create(String name,Integer qty);
    List<OrderView> list();
    OrderView cancel(long id);
}
