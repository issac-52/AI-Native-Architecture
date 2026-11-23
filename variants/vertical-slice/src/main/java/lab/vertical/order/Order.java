package lab.vertical.order;
public class Order {
    private final long id;
    private final String productName;
    private final int quantity;
    private String status = "CREATED";
    public Order(long id, String productName, int quantity) {
        this.id=id; this.productName=productName; this.quantity=quantity;
    }
    public long getId(){return id;}
    public String getProductName(){return productName;}
    public int getQuantity(){return quantity;}
    public synchronized String getStatus(){return status;}
    public synchronized void cancel(){status="CANCELLED";}
}
