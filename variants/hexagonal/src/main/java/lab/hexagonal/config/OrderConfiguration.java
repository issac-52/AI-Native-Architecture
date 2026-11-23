package lab.hexagonal.config;
import lab.hexagonal.application.port.in.OrderUseCases;
import lab.hexagonal.application.port.out.OrderPersistencePort;
import lab.hexagonal.application.service.OrderService;
import org.springframework.context.annotation.*;
@Configuration
public class OrderConfiguration {
    @Bean
    OrderUseCases orderUseCases(OrderPersistencePort storage){return new OrderService(storage);}
}
