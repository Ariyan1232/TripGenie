import { View, Text, StyleSheet, SafeAreaView, TouchableOpacity } from 'react-native';
import { Colors } from '../constants/colors';
import Button from '../components/Button';

export default function HomeScreen({ navigation }) {
  return (
    <SafeAreaView style={styles.safe}>
      <View style={styles.container}>

        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.brandText}>TRIPGENIE</Text>
          <Text style={styles.tagline}>· YOUR TRAVEL PARTNER</Text>
        </View>

        {/* Hero */}
        <View style={styles.hero}>
          <View style={styles.globeContainer}>
            <Text style={styles.globe}>🌐</Text>
            <View style={styles.flightBadge}>
              <Text style={styles.flightBadgeText}>✈ Group travel</Text>
            </View>
          </View>

          <Text style={styles.heroTitle}>Converge</Text>
          <Text style={styles.heroSubtitle}>
            Everyone lands together.{'\n'}No one waits alone.
          </Text>
        </View>

        {/* Actions */}
        <View style={styles.actions}>
          <Button
            title="Create a trip →"
            onPress={() => navigation.navigate('TripSetup')}
          />
          <View style={styles.gap} />
          <Button
            title="Join a trip"
            variant="ghost"
            onPress={() => navigation.navigate('Vote')}
          />
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
    paddingHorizontal: 24,
    paddingBottom: 40,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingTop: 16,
    marginBottom: 8,
  },
  brandText: {
    fontSize: 11,
    fontWeight: '700',
    color: Colors.accent,
    letterSpacing: 2,
  },
  tagline: {
    fontSize: 11,
    color: Colors.textMuted,
    letterSpacing: 1,
  },
  hero: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    gap: 16,
  },
  globeContainer: {
    alignItems: 'center',
    marginBottom: 8,
  },
  globe: {
    fontSize: 96,
  },
  flightBadge: {
    backgroundColor: Colors.surfaceRaised,
    borderWidth: 1,
    borderColor: Colors.accent,
    paddingVertical: 6,
    paddingHorizontal: 14,
    borderRadius: 20,
    marginTop: -12,
  },
  flightBadgeText: {
    fontSize: 12,
    color: Colors.accent,
    fontWeight: '600',
  },
  heroTitle: {
    fontSize: 48,
    fontWeight: '800',
    color: Colors.textPrimary,
    letterSpacing: -1,
    textAlign: 'center',
  },
  heroSubtitle: {
    fontSize: 16,
    color: Colors.textMuted,
    textAlign: 'center',
    lineHeight: 24,
  },
  actions: {
    gap: 12,
  },
  gap: {
    height: 4,
  },
});