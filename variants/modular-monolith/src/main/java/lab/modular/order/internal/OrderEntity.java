package lab.modular.order.internal;
class OrderEntity {
    final long id;
    final String productName;
    final int quantity;
    private String status="CREATED";
    OrderEntity(long id,String name,int qty){this.id=id;productName=name;quantity=qty;}
    synchronized void cancel(){status="CANCELLED";}
    synchronized String getStatus(){return status;}
}
