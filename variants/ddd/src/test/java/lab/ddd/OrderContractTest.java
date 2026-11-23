package lab.ddd;
import lab.contract.OrderContractSuite;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
@SpringBootTest(classes = DddApplication.class)
@AutoConfigureMockMvc
class OrderContractTest extends OrderContractSuite {}
