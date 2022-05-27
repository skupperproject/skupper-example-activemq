package net.example;

import io.quarkus.runtime.QuarkusApplication;
import io.quarkus.runtime.annotations.QuarkusMain;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import javax.enterprise.context.ApplicationScoped;
import org.eclipse.microprofile.reactive.messaging.Channel;
import org.eclipse.microprofile.reactive.messaging.Emitter;
import org.eclipse.microprofile.reactive.messaging.Incoming;

@ApplicationScoped
@QuarkusMain
public class Client implements QuarkusApplication {
    static int desired = 10;
    static CountDownLatch completion = new CountDownLatch(desired);

    @Channel("outgoing-messages")
    Emitter<String> emitter;

    @Override
    public int run(String... args) {
        try {
            for (int i = 1; i <= desired; i++) {
                String message = "message " + i;
                emitter.send(message);
                System.out.println("Sent " + message);
            }

            boolean completed = completion.await(30, TimeUnit.SECONDS);

            if (!completed) {
                System.out.println("Result: Timed out!");
                System.exit(1);
            }

            System.out.println("Result: OK");

            return 0;
        } catch (Exception e) {
            System.out.println("Result: Error!");
            e.printStackTrace();
            return 1;
        }
    }

    @ApplicationScoped
    public static class Receiver {
        @Incoming("incoming-messages")
        public void receive(String message) {
            System.out.println("Received " + message);
            completion.countDown();
        }
    }
}
