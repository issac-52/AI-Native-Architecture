package lab.ddd.order.domain;
/** Aggregate root: owns the cancellation state transition. */
public class OrderAggregate {
    private final long id;
    private final String productName;
    private final int quantity;
    private String status = "CREATED";
    public OrderAggregate(long id,String productName,int quantity){
        this.id=id; this.productName=productName; this.quantity=quantity;
    }
    public long getId(){return id;}
    public String getProductName(){return productName;}
    public int getQuantity(){return quantity;}
    public synchronized String getStatus(){return status;}
    public synchronized void cancel(){status="CANCELLED";}
}
