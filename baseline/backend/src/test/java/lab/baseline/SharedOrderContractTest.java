package lab.baseline;
import lab.contract.OrderContractSuite;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
@SpringBootTest(classes = BaselineApplication.class)
@AutoConfigureMockMvc
class SharedOrderContractTest extends OrderContractSuite {}
