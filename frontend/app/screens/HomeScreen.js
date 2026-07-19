import { View, Text, StyleSheet, SafeAreaView } from 'react-native';
import { Colors } from '../constants/colors';
import Button from '../components/Button';

export default function HomeScreen({ navigation }) {
  return (
    <SafeAreaView style={styles.safe}>
      <View style={styles.container}>

        {/* Top section - branding */}
        <View style={styles.hero}>
          <Text style={styles.logo}>✈</Text>
          <Text style={styles.title}>Converge</Text>
          <Text style={styles.subtitle}>
            Group travel, perfectly synced
          </Text>
        </View>

        {/* Bottom section - actions */}
        <View style={styles.actions}>
          <Text style={styles.prompt}>What would you like to do?</Text>

          <Button
            title="Create a trip"
            onPress={() => navigation.navigate('TripSetup')}
          />

          <View style={styles.divider}>
            <View style={styles.line} />
            <Text style={styles.orText}>or</Text>
            <View style={styles.line} />
          </View>

          <Button
            title="Join a trip"
            variant="secondary"
            onPress={() => navigation.navigate('Join')}
          />

          <Text style={styles.hint}>
            Have a trip code? Tap "Join a trip" to enter it.
          </Text>
        </View>

      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  container: {
    flex: 1,
    paddingHorizontal: 28,
    justifyContent: 'space-between',
    paddingBottom: 48,
  },
  hero: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    gap: 12,
  },
  logo: {
    fontSize: 56,
    marginBottom: 8,
  },
  title: {
    fontSize: 42,
    fontWeight: '700',
    color: Colors.textDark,
    letterSpacing: -1,
  },
  subtitle: {
    fontSize: 17,
    color: Colors.textMuted,
    textAlign: 'center',
    lineHeight: 24,
  },
  actions: {
    gap: 12,
  },
  prompt: {
    fontSize: 14,
    color: Colors.textMuted,
    textAlign: 'center',
    marginBottom: 4,
  },
  divider: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    marginVertical: 4,
  },
  line: {
    flex: 1,
    height: 1,
    backgroundColor: Colors.border,
  },
  orText: {
    fontSize: 13,
    color: Colors.textMuted,
  },
  hint: {
    fontSize: 13,
    color: Colors.textMuted,
    textAlign: 'center',
    marginTop: 4,
  },
});